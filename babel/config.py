# MQTT
MQTT_TOPIC = "ratlantis"

# Box identifiers
BOX_PIGEON   = "pigeon"
BOX_ELEPHANT = "elephant"

# LED hardware
LED_PIN        = 21       # GPIO pin (PWM). Use 10 for SPI (/dev/spidev0.0).
LED_COUNT      = 283
LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 200      # 0–255
LED_INVERT     = False
LED_CHANNEL    = 0

# ── LED Segment Ranges (start, end inclusive) ─────────────────────────────────
# Adjust these to match actual physical wiring.  Everything else derives from them.

# 3 constellation-display surrounds, 4 pixels each
DISPLAY_SURROUND_0 = (0,   3)    # slot 0 / cable1
DISPLAY_SURROUND_1 = (4,   7)    # slot 1 / cable2
DISPLAY_SURROUND_2 = (8,  11)    # slot 2 / cable3

STAR_BG_1      = (12,  36)       # 25-pixel star field before main constellations

CONSTELLATION_A = (37,  51)      # 15 px — puzzle cable1
CONSTELLATION_B = (52,  66)      # 15 px — puzzle cable2

UNUSED_1        = (67,  86)      # 20 px — not rendered

# 6 decorative constellations spread across ~100 pixels
CONSTELLATION_C = ( 87, 101)     # 15 px — puzzle cable3
CONSTELLATION_D = (102, 116)     # 15 px — decorative
CONSTELLATION_E = (117, 131)     # 15 px — decorative
CONSTELLATION_F = (132, 146)     # 15 px — decorative
CONSTELLATION_G = (147, 161)     # 15 px — decorative
CONSTELLATION_H = (162, 176)     # 15 px — decorative

PYRAMID_TOP    = (177, 180)      # 4 px — pyramid accent
INNER_BOX      = (181, 192)      # 12 px — secret box interior
ARROW          = (193, 197)      # 5 px  — arrow pointing to box
BOX_BORDER     = (198, 207)      # 10 px — frame around box front
STAR_BG_2      = (208, 282)      # 75-pixel trailing star field

# ── Constellation puzzle mappings ─────────────────────────────────────────────

# Cable name → display surround LED range (reflects this box's cable status)
CABLE_DISPLAY_MAP = {
    "cable1": DISPLAY_SURROUND_0,
    "cable2": DISPLAY_SURROUND_1,
    "cable3": DISPLAY_SURROUND_2,
}

# Cables that must all be "connected" on both boxes to solve the puzzle
PUZZLE_CABLES = ["cable1", "cable2", "cable3"]

# Constellation name → LED segment.
# Replace placeholder keys with actual constellation names before deployment.
CONSTELLATION_LED_MAP = {
    "placeholder_a": CONSTELLATION_A,
    "placeholder_b": CONSTELLATION_B,
    "placeholder_c": CONSTELLATION_C,
    "placeholder_d": CONSTELLATION_D,
    "placeholder_e": CONSTELLATION_E,
    "placeholder_f": CONSTELLATION_F,
    "placeholder_g": CONSTELLATION_G,
    "placeholder_h": CONSTELLATION_H,
}

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
