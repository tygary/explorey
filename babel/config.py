# MQTT
MQTT_TOPIC = "ratlantis"

# Box identifiers
BOX_PIGEON   = "pigeon"
BOX_ELEPHANT = "elephant"

# LED hardware (shared by both boxes)
LED_PIN        = 10       # GPIO pin. Use 18 for PWM, 10 for SPI (/dev/spidev0.0).
LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 150      # 0–255
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
    "led_count":     253,
    "cable_display": _CABLE_DISPLAY_MAP,
    "star_bgs":     [(12,  24), (62, 136)],
    "box_borders":  [(137, 141), (147, 151)],
    "arrow":         (142, 146),
    "inner_box":     (162, 186),
    "pyramid_top":   (248, 252),
    "unused":       [(56,  61), (152, 161), (226, 227)],
    "constellations": {
        "crab":      (25,  44),
        "infinity":  (45,  55),
        "elephant": (187, 197),
        "worm":     (198, 204),
        "ship":     (205, 216),
        "hole":     (217, 225),
        "pigeon":   (228, 240),
        "stick":    (241, 247),
    },
}

ELEPHANT_LAYOUT = {
    "led_count":     245,
    "cable_display": _CABLE_DISPLAY_MAP,
    "star_bgs":     [(12,  24), (59, 133)],
    "box_borders":  [(140, 144), (150, 154)],
    "arrow":         (145, 149),
    "inner_box":     (159, 181),
    "pyramid_top":   (241, 244),
    "unused":       [(45,  58), (134, 139), (155, 158), (225, 225)],
    "constellations": {
        "pigeon":   (25,  38),
        "worm":     (39,  44),
        "crab":     (182, 197),
        "ship":     (198, 206),
        "infinity": (207, 212),
        "elephant": (213, 224),
        "hole":     (226, 234),
        "stick":    (235, 240),
    },
}

# ── Constellation puzzle ──────────────────────────────────────────────────────
# Cables that must all be "connected" on both boxes to solve the puzzle.
PUZZLE_CABLES = ["cable1", "cable2", "cable3"]

# ── Word puzzle ───────────────────────────────────────────────────────────────
WINNING_COMBO = [5, 8, 9, 3, 6, 2]   # set to actual answer before deployment

# ── Inner box latch ───────────────────────────────────────────────────────────
LATCH_PIN        = 6    # IO6 — HIGH = magnet on (locked), LOW = magnet off (unlocked)
WIN_RESET_SECONDS = 60  # latch stays unlocked for this long, then game resets to init

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
