import json
import logging
import threading
import time

import RPi.GPIO as GPIO

from mqtt.MqttClient import MqttClient
from babel.config import (
    MQTT_TOPIC, BOX_PIGEON, BOX_ELEPHANT,
    PUZZLE_CABLES, WINNING_COMBO,
    PIGEON_LAYOUT, ELEPHANT_LAYOUT,
    STATE_INIT, STATE_PUZZLE_1, STATE_PUZZLE_2,
    STATE_PUZZLE_3, STATE_PUZZLE_4, STATE_COMPLETE,
    LATCH_PIN, WIN_RESET_SECONDS,
)
from babel.led_renderer import LedRenderer
from babel.BabelDmx import BabelDmx
from babel.BabelSoundSystem import BabelSoundSystem
from lighting.DmxControl import DRIVER_ENTTEC, DRIVER_FT232

logger = logging.getLogger(__name__)

_GAME_TIMEOUT_S   = 300   # 5 minutes per puzzle phase
_OUT_OF_TIME_WARN =   5   # seconds before timeout to play warning

_RENDER_FPS = 20
_FRAME_S    = 1.0 / _RENDER_FPS

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
        self._renderer = LedRenderer(PIGEON_LAYOUT if pigeon else ELEPHANT_LAYOUT)
        self._dmx = BabelDmx(driver=DRIVER_ENTTEC if pigeon else DRIVER_FT232)


        # Shared render state (read by render loop, written by MQTT thread)
        self._phase                     = STATE_INIT
        self._own_cable_status          = {}   # {cable: "connected"/"invalid"} for this box
        self._all_constellation_statuses = {}  # {box: {name: "connected"/"invalid"}}

        # Latch — both boxes have one on the same pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(LATCH_PIN, GPIO.OUT)
        GPIO.output(LATCH_PIN, GPIO.HIGH)  # locked on boot

        # Game master state — pigeon only
        if pigeon:
            self._win_cancel         = threading.Event()
            self._timeout_cancel     = threading.Event()
            self._press_ignore_until = 0.0
            self._prev_cable_status  = {BOX_PIGEON: {}, BOX_ELEPHANT: {}}
            self._sound              = BabelSoundSystem()
            self._gs = {
                "phase": STATE_INIT,
                "completed": _empty_completed(),
                "time_target": None,
                "constellation_status": {BOX_PIGEON: {}, BOX_ELEPHANT: {}},
                "cable_status":         {BOX_PIGEON: {}, BOX_ELEPHANT: {}},
                "word_selections": [0, 0, 0, 0, 0, 0],
            }

    def start(self):
        logger.info("Starting BabelController (%s)", self._box)
        self._mqtt = MqttClient(topic=MQTT_TOPIC, hostname="10.0.1.149")
        self._mqtt.listen(self._on_message)
        if self._pigeon:
            self._send_game_update()
        else:
            self._mqtt.publish(json.dumps({"event": "finishedBoot", "box": self._box}))
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
        logger.info("[MQTT IN] %s", payload)

        # Update shared render state for both pigeon and elephant
        with self._lock:
            if event == "gameUpdate":
                self._phase = data.get("state", STATE_INIT)
                # Recover constellation state on reboot
                for b, cs in data.get("constellation_status", {}).items():
                    self._all_constellation_statuses[b] = cs
                self._own_cable_status = data.get("cable_status", {}).get(self._box, {})
                if self._phase == STATE_INIT:
                    self._all_constellation_statuses = {}
                    self._own_cable_status = {}
                if not self._pigeon:
                    GPIO.output(LATCH_PIN, GPIO.LOW if self._phase == STATE_COMPLETE else GPIO.HIGH)
            elif event == "constellationUpdate" and box is not None:
                self._all_constellation_statuses[box] = data.get("connections", {})
                if box == self._box:
                    self._own_cable_status = data.get("cable_status", {})

        # Game master logic — pigeon only
        if self._pigeon:
            self._dispatch(event, box, data)

    def _dispatch(self, event, box, data):
        if event == "finishedBoot":
            self._send_game_update()
        elif event == "buttonPress":
            if time.monotonic() < self._press_ignore_until:
                logger.info("Button press from %s ignored (post-hold cooldown)", box)
            elif self._gs["phase"] == STATE_INIT:
                logger.info("Button press from %s — starting game", box)
                self._transition_to(STATE_PUZZLE_1)
        elif event == "holdButton":
            logger.info("Button hold from %s — resetting to init", box)
            self._press_ignore_until = time.monotonic() + 2.0
            self._transition_to(STATE_INIT)
        elif event == "timeChosen":
            self._on_time_chosen(data.get("hour"), data.get("minute"))
        elif event == "timePuzzleSolved":
            self._on_time_puzzle_solved(box)
        elif event == "artifactPuzzleSolved":
            self._on_artifact_puzzle_solved(box)
        elif event == "constellationUpdate":
            self._on_constellation_update(box, data.get("connections", {}),
                                          data.get("cable_status", {}))
        elif event == "wordKnobChanged" and box is not None:
            # Only handle originals from ESPs (box field present); ignore our own relays
            self._on_word_knob_changed(data.get("dial"), data.get("value"))

    # ── Game master event handlers ────────────────────────────────────────────

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
        self._sound.play_correct_connection()
        self._gs["completed"][box]["artifact"] = True
        self._maybe_advance()

    def _on_constellation_update(self, box, connections, cable_status):
        logger.info("Constellation update: box=%-10s connections=%s", box, connections)
        prev = self._prev_cable_status.get(box, {})
        for cable, status in cable_status.items():
            if status != prev.get(cable):
                if status == "connected":
                    self._sound.play_correct_connection()
                elif status == "invalid":
                    self._sound.play_incorrect_connection()
        self._prev_cable_status[box] = dict(cable_status)
        self._gs["constellation_status"][box] = connections
        self._gs["cable_status"][box]         = cable_status
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
            self._win_cancel.set()
            self._timeout_cancel.set()
            GPIO.output(LATCH_PIN, GPIO.HIGH)
            self._gs["completed"]            = _empty_completed()
            self._gs["time_target"]          = None
            self._gs["constellation_status"] = {BOX_PIGEON: {}, BOX_ELEPHANT: {}}
            self._gs["cable_status"]         = {BOX_PIGEON: {}, BOX_ELEPHANT: {}}
            self._gs["word_selections"]      = [0, 0, 0, 0, 0, 0]
            self._prev_cable_status          = {BOX_PIGEON: {}, BOX_ELEPHANT: {}}
            self._sound.play_reset()
        elif phase == STATE_PUZZLE_1:
            self._sound.play_game_start()
            self._start_puzzle_timer()
        elif phase in (STATE_PUZZLE_2, STATE_PUZZLE_3, STATE_PUZZLE_4):
            self._sound.play_puzzle_complete()
            self._start_puzzle_timer()
        elif phase == STATE_COMPLETE:
            self._timeout_cancel.set()
        self._send_game_update()
        if phase == STATE_COMPLETE:
            self._sound.play_you_win()
            self._run_win_sequence()

    def _all_constellations_correct(self):
        for box in (BOX_PIGEON, BOX_ELEPHANT):
            cs = self._gs["cable_status"][box]
            if not all(cs.get(cable) == "connected" for cable in PUZZLE_CABLES):
                return False
        return True

    def _send_game_update(self):
        msg = {
            "event":                "gameUpdate",
            "state":                self._gs["phase"],
            "time_target":          self._gs["time_target"],
            "constellation_status": self._gs["constellation_status"],
            "cable_status":         self._gs["cable_status"],
            "word_selections":      self._gs["word_selections"],
        }
        logger.info("[MQTT OUT] gameUpdate state=%s", self._gs["phase"])
        self._mqtt.publish(json.dumps(msg))

    def _run_win_sequence(self):
        logger.info("WIN — unlocking inner box latch for %s seconds", WIN_RESET_SECONDS)
        self._win_cancel.clear()
        GPIO.output(LATCH_PIN, GPIO.LOW)

        def expire():
            cancelled = self._win_cancel.wait(WIN_RESET_SECONDS)
            if not cancelled:
                logger.info("Win timer expired — relocking and resetting to init")
                GPIO.output(LATCH_PIN, GPIO.HIGH)
                self._transition_to(STATE_INIT)

        threading.Thread(target=expire, daemon=True).start()

    def _start_puzzle_timer(self):
        self._timeout_cancel.set()
        self._timeout_cancel.clear()

        def _timer():
            cancelled = self._timeout_cancel.wait(_GAME_TIMEOUT_S - _OUT_OF_TIME_WARN)
            if not cancelled:
                self._sound.play_out_of_time()
                cancelled = self._timeout_cancel.wait(_OUT_OF_TIME_WARN)
                if not cancelled:
                    logger.info("Puzzle timer expired — resetting to init")
                    self._transition_to(STATE_INIT)

        threading.Thread(target=_timer, daemon=True).start()

    # ── Render loop ───────────────────────────────────────────────────────────

    def _render_loop(self):
        while True:
            now = time.monotonic()
            with self._lock:
                phase      = self._phase
                own_cables = dict(self._own_cable_status)
                all_cs     = {b: dict(s) for b, s in self._all_constellation_statuses.items()}

            connected = {
                name
                for box_status in all_cs.values()
                for name, status in box_status.items()
                if status == "connected"
            }
            invalid = {
                name for name, status in all_cs.get(self._box, {}).items()
                if status == "invalid"
            }

            self._renderer.render(phase, own_cables, connected, invalid)
            try:
                self._dmx.change_mode(phase)
                self._dmx.update()
            except Exception:
                logger.exception("DMX error")

            elapsed = time.monotonic() - now
            sleep   = _FRAME_S - elapsed
            if sleep > 0:
                time.sleep(sleep)
