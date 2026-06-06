import json
import logging
import threading
import time

from mqtt.MqttClient import MqttClient
from babel.config import (
    MQTT_TOPIC, BOX_PIGEON, BOX_ELEPHANT,
    CORRECT_CONNECTIONS, WINNING_COMBO,
    STATE_INIT, STATE_PUZZLE_1, STATE_PUZZLE_2,
    STATE_PUZZLE_3, STATE_PUZZLE_4, STATE_COMPLETE,
)
from babel.led_renderer import LedRenderer

logger = logging.getLogger(__name__)

_RENDER_FPS = 20
_FRAME_S    = 1.0 / _RENDER_FPS

_EMPTY_CONNECTIONS = {"cable1": None, "cable2": None, "cable3": None}

_PHASE_ORDER = [STATE_PUZZLE_1, STATE_PUZZLE_2, STATE_PUZZLE_3, STATE_PUZZLE_4, STATE_COMPLETE]
_PHASE_KEY   = {
    STATE_PUZZLE_1: "time",
    STATE_PUZZLE_2: "artifact",
    STATE_PUZZLE_3: "constellation",
    STATE_PUZZLE_4: "word",
}


def _empty_completed():
    return {
        BOX_PIGEON:   {"time": False, "artifact": False, "constellation": False, "word": False},
        BOX_ELEPHANT: {"time": False, "artifact": False, "constellation": False, "word": False},
    }


class BabelController:
    def __init__(self, pigeon=True):
        self._pigeon = pigeon
        self._box    = BOX_PIGEON if pigeon else BOX_ELEPHANT
        self._lock   = threading.Lock()
        self._renderer = LedRenderer()

        # Shared render state (read by render loop, written by MQTT thread)
        self._phase           = STATE_INIT
        self._own_connections = dict(_EMPTY_CONNECTIONS)

        # Game master state — pigeon only
        if pigeon:
            self._gs = {
                "phase": STATE_INIT,
                "completed": _empty_completed(),
                "time_target": None,
                "constellation_connections": {
                    BOX_PIGEON:   dict(_EMPTY_CONNECTIONS),
                    BOX_ELEPHANT: dict(_EMPTY_CONNECTIONS),
                },
                "word_selections": [0, 0, 0, 0, 0, 0],
                "hold_start": {BOX_PIGEON: None, BOX_ELEPHANT: None},
            }

    def start(self):
        logger.info("Starting BabelController (%s)", self._box)
        self._mqtt = MqttClient(topic=MQTT_TOPIC, hostname="10.0.1.149")
        self._mqtt.listen(self._on_message)
        threading.Thread(target=self._render_loop, daemon=True).start()

    # ── MQTT ──────────────────────────────────────────────────────────────────

    def _on_message(self, payload):
        try:
            data = json.loads(payload)
        except (ValueError, UnicodeDecodeError):
            logger.warning("Bad MQTT payload: %r", payload)
            return

        event = data.get("event")
        box   = data.get("box")
        logger.info("[MQTT IN] event=%-28s box=%s", event, box or "-")

        # Update shared render state for both pigeon and elephant
        with self._lock:
            if event == "gameUpdate":
                self._phase = data.get("state", STATE_INIT)
                # Restore own constellation connections on reboot recovery
                own = data.get("constellation_connections", {}).get(self._box)
                if own:
                    self._own_connections = own
                if self._phase == STATE_INIT:
                    self._own_connections = dict(_EMPTY_CONNECTIONS)
            elif event == "constellationUpdate" and box == self._box:
                self._own_connections = data.get("connections", dict(_EMPTY_CONNECTIONS))

        # Game master logic — pigeon only
        if self._pigeon:
            self._dispatch(event, box, data)

    def _dispatch(self, event, box, data):
        if event == "finishedBoot":
            self._send_game_update()
        elif event == "holdButton":
            self._on_hold_button(box, data.get("holding", False))
        elif event == "timeChosen":
            self._on_time_chosen(data.get("hour"), data.get("minute"))
        elif event == "timePuzzleSolved":
            self._on_time_puzzle_solved(box)
        elif event == "artifactPuzzleSolved":
            self._on_artifact_puzzle_solved(box)
        elif event == "constellationUpdate":
            self._on_constellation_update(box, data.get("connections", {}))
        elif event == "wordKnobChanged" and box is not None:
            # Only handle originals from ESPs (box field present); ignore our own relays
            self._on_word_knob_changed(data.get("dial"), data.get("value"))

    # ── Game master event handlers ────────────────────────────────────────────

    def _on_hold_button(self, box, holding):
        logger.info("Hold button: box=%-10s holding=%s", box, holding)
        now = time.time()
        if holding:
            self._gs["hold_start"][box] = now
        else:
            start = self._gs["hold_start"][box]
            self._gs["hold_start"][box] = None
            if start is None:
                return
            if now - start >= 5.0:
                logger.info("Long hold — resetting to init")
                self._transition_to(STATE_INIT)
            elif self._gs["phase"] == STATE_INIT:
                logger.info("Button press — starting game")
                self._transition_to(STATE_PUZZLE_1)

    def _on_time_chosen(self, hour, minute):
        logger.info("Time chosen: %02d:%02d", hour or 0, minute or 0)
        self._gs["time_target"] = {"hour": hour, "minute": minute}
        self._send_game_update()

    def _on_time_puzzle_solved(self, box):
        logger.info("Time puzzle SOLVED by %s", box)
        self._gs["completed"][box]["time"] = True
        self._gs["completed"][BOX_ELEPHANT]["time"] = True  # elephant always done once it chose
        self._maybe_advance()

    def _on_artifact_puzzle_solved(self, box):
        logger.info("Artifact puzzle SOLVED by %s", box)
        self._gs["completed"][box]["artifact"] = True
        self._maybe_advance()

    def _on_constellation_update(self, box, connections):
        logger.info("Constellation update: box=%-10s connections=%s", box, connections)
        self._gs["constellation_connections"][box] = connections
        if self._all_constellations_correct():
            logger.info("All constellations CORRECT")
            self._gs["completed"][BOX_PIGEON]["constellation"]   = True
            self._gs["completed"][BOX_ELEPHANT]["constellation"] = True
            self._maybe_advance()

    def _on_word_knob_changed(self, dial, value):
        if dial is None or value is None:
            return
        self._gs["word_selections"][dial] = value
        self._mqtt.publish(json.dumps({"event": "wordKnobChanged", "dial": dial, "value": value}))
        logger.info("Word knob: dial=%s value=%s  selections=%s",
                    dial, value, self._gs["word_selections"])
        if self._gs["word_selections"] == WINNING_COMBO:
            logger.info("Winning word combo entered!")
            self._transition_to(STATE_COMPLETE)

    # ── State machine ─────────────────────────────────────────────────────────

    def _maybe_advance(self):
        key = _PHASE_KEY.get(self._gs["phase"])
        if key and all(self._gs["completed"][b][key] for b in (BOX_PIGEON, BOX_ELEPHANT)):
            idx = _PHASE_ORDER.index(self._gs["phase"])
            next_phase = _PHASE_ORDER[idx + 1]
            logger.info("Both boxes completed '%s' — advancing to %s", key, next_phase)
            self._transition_to(next_phase)

    def _transition_to(self, phase):
        logger.info("Transitioning to %s", phase)
        self._gs["phase"] = phase
        if phase == STATE_INIT:
            self._gs["completed"]                  = _empty_completed()
            self._gs["time_target"]                = None
            self._gs["constellation_connections"]  = {
                BOX_PIGEON:   dict(_EMPTY_CONNECTIONS),
                BOX_ELEPHANT: dict(_EMPTY_CONNECTIONS),
            }
            self._gs["word_selections"] = [0, 0, 0, 0, 0, 0]
            self._gs["hold_start"]      = {BOX_PIGEON: None, BOX_ELEPHANT: None}
        self._send_game_update()
        if phase == STATE_COMPLETE:
            self._run_win_sequence()

    def _all_constellations_correct(self):
        for box in (BOX_PIGEON, BOX_ELEPHANT):
            for cable, correct_plug in CORRECT_CONNECTIONS.items():
                if self._gs["constellation_connections"][box].get(cable) != correct_plug:
                    return False
        return True

    def _send_game_update(self):
        msg = {
            "event":                    "gameUpdate",
            "state":                    self._gs["phase"],
            "time_target":              self._gs["time_target"],
            "constellation_connections": self._gs["constellation_connections"],
            "word_selections":          self._gs["word_selections"],
        }
        logger.info("[MQTT OUT] gameUpdate state=%s", self._gs["phase"])
        self._mqtt.publish(json.dumps(msg))

    def _run_win_sequence(self):
        logger.info("WIN — running win sequence")
        # TODO: trigger relay/servo to open the secret box

    # ── Render loop ───────────────────────────────────────────────────────────

    def _render_loop(self):
        while True:
            now = time.monotonic()
            with self._lock:
                phase       = self._phase
                connections = dict(self._own_connections)
            self._renderer.render(phase, connections)
            elapsed = time.monotonic() - now
            sleep   = _FRAME_S - elapsed
            if sleep > 0:
                time.sleep(sleep)
