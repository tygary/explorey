import random

from lighting.DmxControl import DmxControl
from babel.config import STATE_INIT, STATE_COMPLETE, GAME_RUNNING_STATES

FIXTURE_1 = 10
FIXTURE_2 = 20
FIXTURE_3 = 30
FIXTURES = [FIXTURE_1, FIXTURE_2, FIXTURE_3]

# Colors as [R, G, B, W, A, UV] — tweak these freely
PURPLE = [183,  30, 218, 0, 0, 0]
PINK   = [232,  60, 239, 0, 0, 0]
BLUE   = [ 15, 100, 255, 0, 0, 0]
RED    = [247,   5,  10, 0, 0, 0]
ORANGE = [236, 153,  92, 0, 0, 0]
TEAL   = [  0, 200, 180, 0, 0, 0]

# Static color per fixture for passive (idle) mode
PASSIVE_COLORS = [PURPLE, BLUE, PINK]

# Static color per fixture while the game is running
RUNNING_COLORS = [RED, ORANGE, PURPLE]

# Color per fixture during the win finale (brightness pulses, color stays)
FINALE_COLORS = [RED, PINK, PURPLE]

_MODE_PASSIVE = 0
_MODE_RUNNING = 1
_MODE_FINALE  = 2

# Finale starting brightness offsets so fixtures are never all dark at once
_FINALE_OFFSETS = [0.99, 0.33, 0.66]


class BabelDmx:
    def __init__(self):
        self._dmx = DmxControl()
        self._mode = None
        self._finale_values = list(_FINALE_OFFSETS)
        self._finale_directions = [True, False, True]  # True = increasing
        self._set_passive()

    # ── Private helpers ───────────────────────────────────────────────────────

    def _set_passive(self):
        for i, ch in enumerate(FIXTURES):
            self._dmx.setRfFixture(ch, PASSIVE_COLORS[i])
        self._dmx.render()
        self._mode = _MODE_PASSIVE

    def _set_running(self):
        for i, ch in enumerate(FIXTURES):
            self._dmx.setRfFixture(ch, RUNNING_COLORS[i])
        self._dmx.render()
        self._mode = _MODE_RUNNING

    def _set_finale(self):
        self._finale_values = list(_FINALE_OFFSETS)
        self._finale_directions = [True, False, True]
        for i, ch in enumerate(FIXTURES):
            self._dmx.setRfFixture(ch, FINALE_COLORS[i], int(self._finale_values[i] * 255))
        self._dmx.render()
        self._mode = _MODE_FINALE

    # ── Public API ────────────────────────────────────────────────────────────

    def change_mode(self, phase):
        if phase == STATE_INIT and self._mode != _MODE_PASSIVE:
            self._set_passive()
        elif phase == STATE_COMPLETE and self._mode != _MODE_FINALE:
            self._set_finale()
        elif phase in GAME_RUNNING_STATES and phase != STATE_COMPLETE and self._mode != _MODE_RUNNING:
            self._set_running()

    def update(self):
        if self._mode == _MODE_FINALE:
            for i, ch in enumerate(FIXTURES):
                step = random.random() * 0.04
                if self._finale_directions[i]:
                    self._finale_values[i] += step
                    if self._finale_values[i] >= 1.0:
                        self._finale_values[i] = 1.0
                        self._finale_directions[i] = False
                else:
                    self._finale_values[i] -= step
                    if self._finale_values[i] <= 0.0:
                        self._finale_values[i] = 0.0
                        self._finale_directions[i] = True
                dimmer = int(self._finale_values[i] * 255)
                self._dmx.setRfFixture(ch, FINALE_COLORS[i], dimmer)
            self._dmx.render()
