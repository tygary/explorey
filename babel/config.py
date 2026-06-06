# MQTT
MQTT_TOPIC = "ratlantis"

# Box identifiers
BOX_PIGEON   = "pigeon"
BOX_ELEPHANT = "elephant"

# LED hardware (shared by both boxes)
LED_PIN        = 21       # GPIO pin. Use 18 for PWM, 10 for SPI (/dev/spidev0.0).
LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 200      # 0–255
LED_INVERT     = False
LED_CHANNEL    = 0

# ── LED Layouts ───────────────────────────────────────────────────────────────
# Each layout dict fully describes one physical box's LED strip.
# Edit start/end values here; the renderer derives everything else from them.
#
# Segments are (start, end) inclusive.
# "star_bgs", "box_borders", "unused" are lists — they may appear multiple times.

# Both boxes share the same cable→display-surround mapping at pixels 0-11.
_CABLE_DISPLAY_MAP = {
    "cable1": (8,  11),
    "cable2": (4,   7),
    "cable3": (0,   3),
}

PIGEON_LAYOUT = {
    "led_count":     227,
    "cable_display": _CABLE_DISPLAY_MAP,
    "star_bgs":     [(12,  24), (62, 136)],
    "box_borders":  [(137, 141), (156, 160)],
    "arrow":         (142, 145),
    "inner_box":     (146, 155),
    "pyramid_top":   (222, 226),
    "unused":       [(56,  61), (200, 201)],
    "constellations": {
        "crab":      (25,  44),
        "infinity":  (45,  55),
        "elephant": (161, 171),
        "worm":     (172, 178),
        "spaceship":(179, 190),
        "hole":     (191, 199),
        "pigeon":   (202, 214),
        "stick":    (215, 221),
    },
}

ELEPHANT_LAYOUT = {
    "led_count":     221,
    "cable_display": _CABLE_DISPLAY_MAP,
    "star_bgs":     [(12,  24), (59, 133)],
    "box_borders":  [(134, 138), (153, 157)],
    "arrow":         (139, 142),
    "inner_box":     (143, 152),
    "pyramid_top":   (217, 220),
    "unused":       [(45,  58), (201, 201)],
    "constellations": {
        "pigeon":   (25,  38),
        "worm":     (39,  44),
        "crab":     (158, 173),
        "spaceship":(174, 182),
        "infinity": (183, 188),
        "elephant": (189, 200),
        "hole":     (202, 210),
        "stick":    (211, 216),
    },
}

# ── Constellation puzzle ──────────────────────────────────────────────────────
# Cables that must all be "connected" on both boxes to solve the puzzle.
PUZZLE_CABLES = ["cable1", "cable2", "cable3"]

# ── Word puzzle ───────────────────────────────────────────────────────────────
WINNING_COMBO = [2, 2, 2, 1, 1, 1]   # set to actual answer before deployment

# ── Game state constants ──────────────────────────────────────────────────────
STATE_INIT     = "init"
STATE_PUZZLE_1 = "puzzle1Active"
STATE_PUZZLE_2 = "puzzle2Active"
STATE_PUZZLE_3 = "puzzle3Active"
STATE_PUZZLE_4 = "puzzle4Active"
STATE_COMPLETE = "gameComplete"

GAME_RUNNING_STATES = {
    STATE_PUZZLE_1, STATE_PUZZLE_2, STATE_PUZZLE_3,
    STATE_PUZZLE_4, STATE_COMPLETE,
}
