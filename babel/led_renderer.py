from lighting.PixelControl import PixelControl
from lighting.Colors import Colors
from lighting.routines import BlackoutRoutine, ColorRoutine, PulseRoutine
from lighting.routines.TwinkleRoutine import (
    TwinkleRoutine, TWINKLE_DEFAULT_COLORS, TWINKLE_RAINBOW_COLORS,
)

from babel.config import (
    LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, LED_CHANNEL,
    STATE_COMPLETE, GAME_RUNNING_STATES,
)

_GREEN_COLORS = [
    [0, 255,  70],
    [0, 220,  80],
    [50, 255, 100],
    [0, 190,  60],
]


def _addrs(seg):
    start, end = seg
    return list(range(start, end + 1))


def _addrs_many(segs):
    result = []
    for seg in segs:
        result.extend(_addrs(seg))
    return result


class LedRenderer:
    def __init__(self, layout):
        self._pixels = PixelControl(
            layout["led_count"], LED_BRIGHTNESS, LED_PIN, LED_DMA
        )

        # ── Star backgrounds ──────────────────────────────────────────────────
        star_addrs = _addrs_many(layout["star_bgs"])
        self._stars = {
            "twinkle": TwinkleRoutine(self._pixels, star_addrs,
                                      colors=TWINKLE_DEFAULT_COLORS, max_brightness=0.3),
            "rainbow": TwinkleRoutine(self._pixels, star_addrs,
                                      colors=TWINKLE_RAINBOW_COLORS, max_brightness=0.3),
        }

        # ── Display surrounds — one dict per cable ────────────────────────────
        self._surrounds = {}
        for cable, seg in layout["cable_display"].items():
            addrs = _addrs(seg)
            self._surrounds[cable] = {
                "off":       BlackoutRoutine(self._pixels, addrs),
                "connected": ColorRoutine(self._pixels, addrs, color=Colors.green),
                "invalid":   PulseRoutine(self._pixels, addrs, color=Colors.red, rate=0.15),
            }

        # ── Constellations — one dict per named constellation ─────────────────
        self._constellation_routines = {}
        for name, seg in layout["constellations"].items():
            addrs = _addrs(seg)
            self._constellation_routines[name] = {
                "idle":      TwinkleRoutine(self._pixels, addrs,
                                            colors=TWINKLE_DEFAULT_COLORS, max_brightness=0.3),
                "connected": ColorRoutine(self._pixels, addrs, color=Colors.green),
                "invalid":   PulseRoutine(self._pixels, addrs, color=Colors.red, rate=0.15),
                "rainbow":   TwinkleRoutine(self._pixels, addrs,
                                            colors=TWINKLE_RAINBOW_COLORS, max_brightness=0.3),
            }

        # ── Pyramid top ───────────────────────────────────────────────────────
        pyramid_addrs = _addrs(layout["pyramid_top"])
        self._pyramid = {
            "blue":    ColorRoutine(self._pixels, pyramid_addrs, color=Colors.blue),
            "red":     ColorRoutine(self._pixels, pyramid_addrs, color=Colors.red),
            "rainbow": TwinkleRoutine(self._pixels, pyramid_addrs,
                                      colors=TWINKLE_RAINBOW_COLORS, max_brightness=0.3),
        }

        # ── Inner box ─────────────────────────────────────────────────────────
        inner_addrs = _addrs(layout["inner_box"])
        self._inner_box = {
            "off":   BlackoutRoutine(self._pixels, inner_addrs),
            "white": ColorRoutine(self._pixels, inner_addrs, color=Colors.white),
        }

        # ── Arrow ─────────────────────────────────────────────────────────────
        arrow_addrs = _addrs(layout["arrow"])
        self._arrow = {
            "idle":  PulseRoutine(self._pixels, arrow_addrs, color=[150, 150, 150], rate=0.02),
            "flash": PulseRoutine(self._pixels, arrow_addrs, color=Colors.green, rate=0.15),
        }

        # ── Box border (both segments combined) ───────────────────────────────
        border_addrs = _addrs_many(layout["box_borders"])
        self._box_border = {
            "idle":  PulseRoutine(self._pixels, border_addrs, color=[150, 150, 150], rate=0.02),
            "green": PulseRoutine(self._pixels, border_addrs, color=Colors.green, rate=0.03),
        }

        # ── Unused gaps — always black ────────────────────────────────────────
        self._unused = BlackoutRoutine(self._pixels, _addrs_many(layout["unused"]))

    def render(self, game_state, own_cable_status, connected_constellations, invalid_constellations):
        """
        game_state               — STATE_* string
        own_cable_status         — {cable: "connected"/"invalid"} for this box
        connected_constellations — set of names connected by any box → green twinkle
        invalid_constellations   — set of names invalid on this box  → red flash
        """
        is_running  = game_state in GAME_RUNNING_STATES
        is_complete = game_state == STATE_COMPLETE

        # Stars
        self._stars["rainbow" if is_complete else "twinkle"].tick()

        # Display surrounds — cable status on this box only
        for cable, routines in self._surrounds.items():
            routines.get(own_cable_status.get(cable), routines["off"]).tick()

        # Constellations — cross-box connected = green, own invalid = red
        for name, routines in self._constellation_routines.items():
            if is_complete:
                routines["rainbow"].tick()
            elif name in connected_constellations:
                routines["connected"].tick()
            elif name in invalid_constellations:
                routines["invalid"].tick()
            else:
                routines["idle"].tick()

        # Pyramid top
        if is_complete:
            self._pyramid["rainbow"].tick()
        elif is_running:
            self._pyramid["red"].tick()
        else:
            self._pyramid["blue"].tick()

        # Inner box
        self._inner_box["white" if is_complete else "off"].tick()

        # Arrow
        self._arrow["flash" if is_complete else "idle"].tick()

        # Box border
        self._box_border["green" if is_complete else "idle"].tick()

        # Unused gaps
        self._unused.tick()

        self._pixels.render()
