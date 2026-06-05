import math
import random

from lighting.routines.Routine import Routine

# Default: four white-ish tints for a starfield feel
TWINKLE_DEFAULT_COLORS = [
    [255, 248, 235],  # warm cream
    [235, 245, 255],  # cool blue-white
    [255, 255, 225],  # warm white
    [235, 255, 248],  # hint of teal
]

TWINKLE_RAINBOW_COLORS = [
    [255,  0,   0],
    [255, 100,  0],
    [220, 220,  0],
    [0,   255,  0],
    [0,   80,  255],
    [80,   0,  255],
    [180,  0,  180],
]

_TWO_PI = 2.0 * math.pi
_FPS = 20


class TwinkleRoutine(Routine):
    """
    Each LED independently oscillates in brightness via a sine wave,
    with a random period and a random color drawn from the colors list.
    Brightness ranges from 0 up to max_brightness.
    """

    def __init__(self, pixels, addresses, colors=None, max_brightness=0.3,
                 min_period=0.5, max_period=10.0,
                 should_override=False, brightness=1.0):
        super().__init__(pixels, addresses, should_override, brightness)
        self._colors = colors if colors is not None else TWINKLE_DEFAULT_COLORS
        self._max_brightness = max_brightness

        self._phases = []
        self._speeds = []
        self._light_colors = []

        for _ in addresses:
            self._phases.append(random.uniform(0, _TWO_PI))
            period_frames = random.uniform(min_period * _FPS, max_period * _FPS)
            self._speeds.append(_TWO_PI / period_frames)
            self._light_colors.append(list(random.choice(self._colors)))

    def tick(self):
        for i, address in enumerate(self.addresses):
            self._phases[i] = (self._phases[i] + self._speeds[i]) % _TWO_PI
            b = self._max_brightness * (math.sin(self._phases[i]) + 1.0) / 2.0
            c = self._light_colors[i]
            self.pixels.setColor(address, [int(b * c[0]), int(b * c[1]), int(b * c[2])])
