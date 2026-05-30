import json
import logging
import threading
import time

from mqtt.MqttClient import MqttClient
from babel.config import MQTT_TOPIC, CORRECT_CONNECTIONS, STATE_INIT
from babel.led_renderer import LedRenderer

logger = logging.getLogger(__name__)

_RENDER_FPS = 20
_FRAME_S    = 1.0 / _RENDER_FPS


class BabelController:
    def __init__(self):
        self._game_state  = STATE_INIT
        self._connections = {cable: None for cable in CORRECT_CONNECTIONS}
        self._lock        = threading.Lock()
        self._renderer    = LedRenderer()

    def start(self):
        self._mqtt = MqttClient(topic=MQTT_TOPIC, hostname="127.0.0.1")
        self._mqtt.listen(self._on_message)
        threading.Thread(target=self._render_loop, daemon=True).start()

    # ── MQTT ──────────────────────────────────────────────────────────────────

    def _on_message(self, payload):
        try:
            data = json.loads(payload)
        except (ValueError, UnicodeDecodeError):
            return

        event = data.get("event")
        if event == "gameUpdate":
            state = data.get("state", STATE_INIT)
            with self._lock:
                logger.info("Game state → %s", state)
                self._game_state = state
                if state == STATE_INIT:
                    self._connections = {cable: None for cable in CORRECT_CONNECTIONS}
        elif event == "constellationUpdate":
            with self._lock:
                for cable, plug in data.get("connections", {}).items():
                    self._connections[cable] = plug

    # ── Render loop ───────────────────────────────────────────────────────────

    def _render_loop(self):
        while True:
            now = time.monotonic()
            with self._lock:
                state       = self._game_state
                connections = dict(self._connections)
            self._renderer.render(state, connections)
            elapsed = time.monotonic() - now
            sleep   = _FRAME_S - elapsed
            if sleep > 0:
                time.sleep(sleep)
