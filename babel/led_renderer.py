from lighting.PixelControl import PixelControl
from lighting.Colors import Colors
from lighting.routines import (
    BlackoutRoutine, ColorRoutine, PulseRoutine,
)
from lighting.routines.TwinkleRoutine import (
    TwinkleRoutine, TWINKLE_DEFAULT_COLORS, TWINKLE_RAINBOW_COLORS,
)

from babel.config import (
    LED_PIN, LED_COUNT, LED_BRIGHTNESS, LED_DMA,
    CABLE_CONSTELLATION_MAP, CORRECT_CONNECTIONS,
    DISPLAY_SURROUND_0, DISPLAY_SURROUND_1, DISPLAY_SURROUND_2,
    STAR_BG_1, STAR_BG_2,
    CONSTELLATION_A, CONSTELLATION_B, CONSTELLATION_C,
    CONSTELLATION_D, CONSTELLATION_E, CONSTELLATION_F,
    CONSTELLATION_G, CONSTELLATION_H,
    PYRAMID_TOP, INNER_BOX, ARROW, BOX_BORDER,
    UNUSED_1,
    STATE_COMPLETE, STATE_PUZZLE_3, GAME_RUNNING_STATES,
)

_CABLE_ORDER = ["cable1", "cable2", "cable3"]
_SURROUND_SEGS = [DISPLAY_SURROUND_0, DISPLAY_SURROUND_1, DISPLAY_SURROUND_2]
_PUZZLE_CONST_SEGS = [CONSTELLATION_A, CONSTELLATION_B, CONSTELLATION_C]
_DECO_CONST_SEGS = [CONSTELLATION_D, CONSTELLATION_E, CONSTELLATION_F,
                    CONSTELLATION_G, CONSTELLATION_H]

_GREEN_COLORS = [
    [0, 255,  70],
    [0, 220,  80],
    [50, 255, 100],
    [0, 190,  60],
]


def _addrs(seg):
    start, end = seg
    return list(range(start, end + 1))


class LedRenderer:
    def __init__(self):
        self._pixels = PixelControl(LED_COUNT, LED_BRIGHTNESS, LED_PIN, LED_DMA)

        # ── Stars ─────────────────────────────────────────────────────────────
        star_addrs = _addrs(STAR_BG_1) + _addrs(STAR_BG_2)
        self._stars = {
            "twinkle": TwinkleRoutine(self._pixels, star_addrs,
                                      colors=TWINKLE_DEFAULT_COLORS, max_brightness=0.3),
            "rainbow": TwinkleRoutine(self._pixels, star_addrs,
                                      colors=TWINKLE_RAINBOW_COLORS, max_brightness=0.3),
        }

        # ── Display surrounds (one dict per slot) ─────────────────────────────
        self._surrounds = []
        for seg in _SURROUND_SEGS:
            addrs = _addrs(seg)
            self._surrounds.append({
                "off":     BlackoutRoutine(self._pixels, addrs),
                "active":  PulseRoutine(self._pixels, addrs, color=Colors.purple, rate=0.03),
                "correct": ColorRoutine(self._pixels, addrs, color=Colors.green),
            })

        # ── Puzzle constellations A/B/C (one dict per cable) ──────────────────
        self._puzzle_constellations = []
        for seg in _PUZZLE_CONST_SEGS:
            addrs = _addrs(seg)
            self._puzzle_constellations.append({
                "idle":    TwinkleRoutine(self._pixels, addrs,
                                         colors=TWINKLE_DEFAULT_COLORS, max_brightness=0.3),
                "correct": TwinkleRoutine(self._pixels, addrs,
                                         colors=_GREEN_COLORS, max_brightness=0.7),
                "rainbow": TwinkleRoutine(self._pixels, addrs,
                                         colors=TWINKLE_RAINBOW_COLORS, max_brightness=0.3),
            })

        # ── Decorative constellations D–H ─────────────────────────────────────
        deco_addrs = sum((_addrs(seg) for seg in _DECO_CONST_SEGS), [])
        self._deco_constellations = {
            "idle":    TwinkleRoutine(self._pixels, deco_addrs,
                                     colors=TWINKLE_DEFAULT_COLORS, max_brightness=0.3),
            "rainbow": TwinkleRoutine(self._pixels, deco_addrs,
                                     colors=TWINKLE_RAINBOW_COLORS, max_brightness=0.3),
        }

        # ── Pyramid top ───────────────────────────────────────────────────────
        pyramid_addrs = _addrs(PYRAMID_TOP)
        self._pyramid = {
            "blue":    ColorRoutine(self._pixels, pyramid_addrs, color=Colors.blue),
            "red":     ColorRoutine(self._pixels, pyramid_addrs, color=Colors.red),
            "rainbow": TwinkleRoutine(self._pixels, pyramid_addrs,
                                     colors=TWINKLE_RAINBOW_COLORS, max_brightness=0.3),
        }

        # ── Inner box ─────────────────────────────────────────────────────────
        inner_addrs = _addrs(INNER_BOX)
        self._inner_box = {
            "off":   BlackoutRoutine(self._pixels, inner_addrs),
            "white": ColorRoutine(self._pixels, inner_addrs, color=Colors.white),
        }

        # ── Arrow ─────────────────────────────────────────────────────────────
        arrow_addrs = _addrs(ARROW)
        self._arrow = {
            "idle":  PulseRoutine(self._pixels, arrow_addrs, color=[150, 150, 150], rate=0.02),
            "green": PulseRoutine(self._pixels, arrow_addrs, color=Colors.green,   rate=0.03),
        }

        # ── Box border ────────────────────────────────────────────────────────
        border_addrs = _addrs(BOX_BORDER)
        self._box_border = {
            "idle":  PulseRoutine(self._pixels, border_addrs, color=[150, 150, 150], rate=0.02),
            "green": PulseRoutine(self._pixels, border_addrs, color=Colors.green,   rate=0.03),
        }

        # ── Unused — always black ─────────────────────────────────────────────
        self._unused = BlackoutRoutine(self._pixels, _addrs(UNUSED_1))

    def render(self, game_state, connections):
        """Tick every active routine for this frame, then flush to the strip."""
        is_running   = game_state in GAME_RUNNING_STATES
        is_complete  = game_state == STATE_COMPLETE
        is_c3_active = game_state == STATE_PUZZLE_3

        correct = {
            cable: (connections.get(cable) == CORRECT_CONNECTIONS[cable])
            for cable in _CABLE_ORDER
        }

        # Stars
        self._stars["rainbow" if is_complete else "twinkle"].tick()

        # Display surrounds — per slot
        for i, cable in enumerate(_CABLE_ORDER):
            if correct[cable]:
                key = "correct"
            elif is_c3_active:
                key = "active"
            else:
                key = "off"
            self._surrounds[i][key].tick()

        # Puzzle constellations — per cable
        for i, cable in enumerate(_CABLE_ORDER):
            if is_complete:
                key = "rainbow"
            elif correct[cable]:
                key = "correct"
            else:
                key = "idle"
            self._puzzle_constellations[i][key].tick()

        # Decorative constellations
        self._deco_constellations["rainbow" if is_complete else "idle"].tick()

        # Pyramid
        if is_complete:
            self._pyramid["rainbow"].tick()
        elif is_running:
            self._pyramid["red"].tick()
        else:
            self._pyramid["blue"].tick()

        # Inner box
        self._inner_box["white" if is_complete else "off"].tick()

        # Arrow
        self._arrow["green" if is_complete else "idle"].tick()

        # Box border
        self._box_border["green" if is_complete else "idle"].tick()

        # Unused gap
        self._unused.tick()

        self._pixels.render()
