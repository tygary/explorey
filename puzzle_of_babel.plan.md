# Ratlantis Game — Implementation Plan

## Overview

Five devices: four ESP boards (one per puzzle) and a Raspberry Pi. Communication happens via MQTT over WiFi on a shared topic (`ratlantis`). The Time Puzzle ESP acts as the **game master** — it holds the start button and is responsible for broadcasting `gameUpdate` events that advance global state. The Raspberry Pi runs the MQTT broker and handles constellation LED rendering, win celebration lighting, and opening a secret box.

---

## Game Flow

```
GAME_INIT          → (button press on Puzzle 1) → PUZZLE_1_ACTIVE
PUZZLE_1_ACTIVE    → (time set correctly)        → PUZZLE_2_ACTIVE
PUZZLE_2_ACTIVE    → (all artifacts attached)    → PUZZLE_3_ACTIVE
PUZZLE_3_ACTIVE    → (all cables plugged in)     → PUZZLE_4_ACTIVE
PUZZLE_4_ACTIVE    → (correct words set)         → GAME_COMPLETE
```

Reset: hold the button on Puzzle 1 for 5 seconds at any time → `GAME_INIT`

---

## Per-Board Modes

Every ESP board uses the same top-level mode constants:

| Constant            | Value | Meaning                                    |
|---------------------|-------|--------------------------------------------|
| `MODE_INITIALIZING` | -1    | Booting, waiting for WiFi/MQTT             |
| `MODE_PASSIVE`      |  0    | Game not started, idle                     |
| `MODE_WAITING`      |  1    | Game started but this puzzle is not active |
| `MODE_PLAYING`      |  2    | This puzzle is active                      |
| `MODE_COMPLETED`    |  3    | This puzzle has been solved                |

---

## MQTT Message Design

**Topic:** `ratlantis` (all boards and the Pi publish and subscribe to the same topic)

### Game Master → All (from Time Puzzle ESP)

```json
{ "event": "gameUpdate", "state": "<state_string>" }
```

State strings: `"init"`, `"puzzle1Active"`, `"puzzle2Active"`, `"puzzle3Active"`, `"puzzle4Active"`, `"gameComplete"`

The game master also broadcasts `gameStart` when the button is first pressed (before puzzle 1 activates), so all boards can transition out of `MODE_PASSIVE` to `MODE_WAITING`.

### Individual Puzzle Commands (targeted, any sender)

```json
{ "event": "puzzleUpdate", "id": "<puzzle_name>", "command": "reset" | "gameStart" | "gameUpdate" }
```

### Puzzle 1 (Time) → All

```json
{ "event": "gameStart", "id": "time_puzzle" }
{ "event": "timePuzzleSolved", "id": "time_puzzle" }
```

### Puzzle 2 (Artifact) → All

```json
{ "event": "artifactSlotUpdate", "id": "artifact_puzzle", "slot": 0, "connected": true, "valid": true }
{ "event": "artifactPuzzleSolved", "id": "artifact_puzzle" }
```

### Puzzle 3 (Constellation) → All (including Pi LED renderer)

Sent on every change to cable connections:

```json
{ "event": "constellationUpdate", "id": "constellation_puzzle",
  "connections": { "cable1": "<plug_pin>", "cable2": null, "cable3": "<plug_pin>" } }
```

`null` means that cable is unplugged. Plug values are the `fern.D*` pin constant values.

```json
{ "event": "constellationPuzzleSolved", "id": "constellation_puzzle" }
```

### Puzzle 4 (Word) → All

```json
{ "event": "wordPuzzleCompleted", "id": "babel_word_puzzle" }
```

---

## Puzzle 1 — Time Puzzle

**File:** `babel_time_puzzle.py` | **Class:** `BabelTimePuzzle`

### Hardware

| Component               | Connection                                      |
|-------------------------|-------------------------------------------------|
| Start/reset button      | `fern.D1`, shorts to GND (active low, PULL_UP) |
| LargeDisplay            | Direct I2C (no mux), addr `0x3C` via `NoMux`   |
| RotaryEncoder (hour)    | Direct I2C, addr `0x36`                         |
| RotaryEncoder (minute)  | Direct I2C, addr `0x37`                         |
| LED strip               | `LED1_DATA`, 73 LEDs total                      |

The two encoders use different I2C addresses (solder-jumper configured) so no mux or lock is needed. The `LargeDisplay` is wrapped with `NoMux` (from `i2c_mux`) to give the display the same interface as mux-backed displays without the overhead.

### LED Layout (73 total)

| LEDs   | Purpose                          | Color                              |
|--------|----------------------------------|------------------------------------|
| 0–1    | Minute symbol indicator          | Yellow                             |
| 2–3    | Hour symbol indicator            | Green                              |
| 4–5    | Unused                           | —                                  |
| 6–9    | Surround start button            | Green in `MODE_PASSIVE`, else off  |
| 10–24  | Ignored                          | Off                                |
| 25–72  | Analog clock face (12 × 4 LEDs) | See below                          |

**Clock face segments** — `CLOCK_FACE_START = 25`, each position `h` (0–11):

| Segment                  | LEDs                                | Purpose                   |
|--------------------------|-------------------------------------|---------------------------|
| `seg_clock[h]`           | `25 + h*4` … `25 + h*4 + 3` (4)    | Full position (minute)    |
| `seg_clock_inner[h]`     | `25 + h*4 + 2` … `25 + h*4 + 3` (2)| Inner two (hour hand)     |
| `seg_clock_outer[h]`     | `25 + h*4` … `25 + h*4 + 1` (2)    | Outer two (overlap case)  |

**Render rules** for hour position `h` and minute position `m`:
- `h == m` (overlap): outer two = yellow (minute), inner two = green (hour)
- `pos == h` only: inner two = green
- `pos == m` only: all four = yellow
- Otherwise: all four = dim idle pattern (alpha 0.1)

### Display

`LargeDisplay` renders two 64×64 symbol images side by side (left = hour, right = minute). Symbols are P4 PBM files at `symbols/clock_N.pbm` where N is 1–12. Position `0` maps to `clock_12.pbm`.

### Button Behaviour

Polled every 50 ms (`BUTTON_POLL_MS = 50`). Active low (pin reads `0` when pressed).

- **Short press (released before 5 s):** In `MODE_PASSIVE`, broadcasts `gameStart` and transitions to `MODE_PLAYING`.
- **Hold ≥ 5 s (`BUTTON_HOLD_MS = 5000`):** Broadcasts `gameUpdate` with `state: "init"` and resets all positions to 0.

### Winning Condition

```python
WINNING_HOUR   = 3   # 3 o'clock
WINNING_MINUTE = 7   # 7 × 5 = 35 minutes
```

Win when `hour_position == WINNING_HOUR and minute_position == WINNING_MINUTE`. Broadcasts `timePuzzleSolved`. The game master logic in `_handle_puzzle_solved` then immediately broadcasts `gameUpdate` with `state: "puzzle2Active"`.

### Role as Game Master

`_handle_puzzle_solved(event)` listens for all four puzzle completion events and broadcasts the corresponding `gameUpdate`:

```python
{
    "timePuzzleSolved":        "puzzle2Active",
    "artifactPuzzleSolved":    "puzzle3Active",
    "constellationPuzzleSolved": "puzzle4Active",
    "wordPuzzleCompleted":     "gameComplete",
}
```

---

## Puzzle 2 — Artifact Puzzle

**File:** `babel_artifact_puzzle.py` | **Class:** `BabelArtifactPuzzle`

### Hardware

| Component         | Connection                                    |
|-------------------|-----------------------------------------------|
| MediumDisplay × 3 | I2C via MUX, ports 1–3                        |
| RFID scanner × 3  | I2C via MUX, ports 4–6                        |
| Magnet × 3        | GPIO pins (passed as `magnet_pins` tuple)     |
| LED strip         | `LED1_DATA`, 21 LEDs                          |

All six I2C devices (3 displays + 3 RFID readers) share the same `I2CMux`. A single `asyncio.Lock()` (`i2c_lock`) is shared across all three `I2cRfidReader` tasks to prevent concurrent mux port switching.

### LED Layout (21 total)

Slots follow a stride-7 pattern: slot `i` starts at LED `7 * i`.

| LEDs     | Purpose              |
|----------|----------------------|
| 0–3      | Surround display 1   |
| 4–6      | Surround RFID 1      |
| 7–10     | Surround display 2   |
| 11–13    | Surround RFID 2      |
| 14–17    | Surround display 3   |
| 18–20    | Surround RFID 3      |

```python
seg_display[i] = canopy.Segment(0, 7 * i,     4)
seg_rfid[i]    = canopy.Segment(0, 7 * i + 4, 3)
```

### `I2cRfidReader`

Lightweight I2C poller (defined in `babel_artifact_puzzle.py`, not imported from anywhere):

```python
READER_ADDR = 0x60   # PN532-compatible I2C address
TAG_REG     = 0x10   # register holding the current UID
TAG_LEN     = 8      # bytes; all-zero = no tag present
```

Polls every 200 ms. On mux port select → `i2c.readfrom_mem()` → deselect. Fires `on_tag_found(uid_hex_string)` / `on_tag_lost()` callbacks when the detected UID changes.

### `ArtifactSlot`

Per-slot state machine (also defined inline in `babel_artifact_puzzle.py`):

| State         | Value | Meaning                           |
|---------------|-------|-----------------------------------|
| `SLOT_OFF`    | 0     | Puzzle not yet active             |
| `SLOT_WAITING`| 1     | Active, no tag present            |
| `SLOT_CORRECT`| 2     | Correct tag detected, magnet held |
| `SLOT_INVALID`| 3     | Wrong tag, magnet released        |

Magnet control via `rat_magnet.Magnet` (that utility is small enough to import directly). `render(patterns, params)` draws both LED segments for the slot based on current state.

### LED Patterns (CTP strings)

The CTP pattern strings for this puzzle are **placeholders** in the current code and need to be replaced with actual canopy tool output before deployment:

- `_PAT_INITIALIZING`, `_PAT_OFF`, `_PAT_WAITING`, `_PAT_CORRECT`, `_PAT_INVALID`, `_PAT_COMPLETED`

Semantic mapping per slot state:
- `SLOT_OFF`     → `pat_off` (dim ambient, α=0.3)
- `SLOT_WAITING` → `pat_waiting` (slow animated pulse, α=0.8)
- `SLOT_CORRECT` → `pat_correct` (solid celebration, α=1.0)
- `SLOT_INVALID` → `pat_invalid` (red flash, α=1.0)

### Expected RFID Tags

```python
EXPECTED_TAGS = ["aabbccdd", "11223344", "55667788"]   # replace with real UIDs
```

### Display

Each `MediumDisplay` shows a 128×128 symbol image from `artifacts/slot_N.pbm` (P4 PBM). Images are loaded fresh on each display update (no caching, to keep RAM low on the ESP).

### Winning Condition

All three slots in `SLOT_CORRECT`. Checked after every `EVENT_SLOT_CHANGED`. Broadcasts `artifactPuzzleSolved`.

---

## Puzzle 3 — Constellation Puzzle

**File:** `babel_constellation_puzzle.py` | **Class:** `BabelConstellationPuzzle`

### Hardware

| Component         | Connection                                      |
|-------------------|-------------------------------------------------|
| MediumDisplay × 3 | I2C via MUX, ports 1–3                          |
| Cable pins        | `fern.D1`, `D2`, `D3` — GPIO outputs, probe HIGH |
| Plug pins         | `fern.D4`, `D5`, `D6`, `D7` — GPIO inputs, PULL_DOWN |

**No local LEDs.** The Raspberry Pi handles all constellation LED rendering for this puzzle based on MQTT messages.

### Cable Detection Algorithm

Polling task at `POLL_INTERVAL = 0.1 s`, settle delay `CABLE_SETTLE_S = 0.005 s`:

```python
for i, cable_obj in enumerate(self._cable_pin_objs):
    cable_obj.on()                          # drive HIGH
    await asyncio.sleep(CABLE_SETTLE_S)
    found_plug = None
    for j, plug_obj in enumerate(self._plug_pin_objs):
        if plug_obj.value() == 1:
            found_plug = PLUG_PINS[j]
            break
    cable_obj.off()
    new_connections[CABLE_PINS[i]] = found_plug
```

If `new_connections != self._connections`, updates state and calls `_update_state(EVENT_CONNECTIONS_CHANGED)`.

### Correct Answer

```python
CORRECT_CONNECTIONS = {fern.D1: fern.D4, fern.D2: fern.D6, fern.D3: fern.D5}
```

Human-readable names for MQTT serialisation:
```python
CABLE_NAMES = {fern.D1: "cable1", fern.D2: "cable2", fern.D3: "cable3"}
```

### MQTT Behaviour

Every time connections change (any cable plugged/unplugged):
```json
{ "event": "constellationUpdate", "id": "constellation_puzzle",
  "connections": { "cable1": "<plug_pin_value>", "cable2": null, "cable3": "<plug_pin_value>" } }
```

On win:
```json
{ "event": "constellationPuzzleSolved", "id": "constellation_puzzle" }
```

### Display

Each `MediumDisplay` shows a 128×128 symbol image from `constellations/slot_N.pbm` (P4 PBM) indicating which plug its cable should go into.

### Winning Condition

`self._connections == CORRECT_CONNECTIONS` for all three cables simultaneously.

---

## Puzzle 4 — Word Puzzle

**File:** `babel_word_puzzle.py` | **Class:** `BabelWordPuzzle`

Three `MediumDisplay` screens + three `RotaryEncoder` knobs. All encoders share I2C address `0x36` and are isolated by mux ports (shared `asyncio.Lock()` required). Activates on `gameUpdate` with `state: "puzzle4Active"`. Broadcasts `wordPuzzleCompleted` on win.

The word lists and winning combination (`WINNING_COMBO = (0, 0, 0)`) are hardcoded and need to be set to the actual puzzle content before deployment.

---

## Raspberry Pi

The Pi has three responsibilities: MQTT broker, constellation LED rendering, and the win sequence.

### MQTT Broker

Run **Mosquitto** on the Pi. All five devices (4 ESPs + Pi itself as a client) connect to it.

```
# /etc/mosquitto/mosquitto.conf
listener 1883
allow_anonymous true
```

The Pi's Python client also subscribes to `ratlantis` to drive the LED and box logic.

### Constellation LED Rendering

The Pi controls an LED strip that physically surrounds or represents the three constellation stations. It listens for `constellationUpdate` messages and lights up each constellation's LEDs as its cable is correctly connected.

**Message consumed:**
```json
{ "event": "constellationUpdate", "connections": { "cable1": "...", "cable2": null, "cable3": "..." } }
```

**Rendering logic:** For each cable, compare its connected plug against the correct plug. If correct, illuminate that constellation's LEDs with a "solved" pattern; if incorrect or unplugged, show a dim or off state.

The correct plug mapping must be mirrored on the Pi so it knows which `cable→plug` pair means "solved" for each constellation.

**Message consumed for final state:**
```json
{ "event": "constellationPuzzleSolved" }
```

On this event, run a celebration pattern across all constellation LEDs.

### Win Sequence

On receiving:
```json
{ "event": "gameUpdate", "state": "gameComplete" }
```

The Pi executes the win sequence in order:

1. **Celebration lighting** — run a full win animation on all Pi-controlled LEDs (could span the whole room or just the constellation strip, depending on wiring).
2. **Secret box** — trigger a relay or servo to open the box. This could be a GPIO output connected to a solenoid lock, a servo, or a relay board.

**Example (relay on GPIO pin 17):**
```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)   # energise to unlock
```

### Pi Software Structure

```
ratlantis_pi/
├── main.py               # entry point, starts broker client + tasks
├── mqtt_client.py        # wraps paho-mqtt, dispatches events
├── constellation_leds.py # LED strip control for constellation puzzle
├── win_sequence.py       # celebration lights + box trigger
└── config.py             # MQTT host, pin numbers, correct connection map
```

The Pi client uses **paho-mqtt** (not MicroPython's `umqtt`). The LED strip is driven with **rpi_ws281x** or **neopixel** library depending on the strip type.

---

## Code Architecture (ESP Boards)

All four puzzle files follow the same structure:

```
class Babel<PuzzleName>:
    current_mode = MODE_INITIALIZING

    def __init__(self, name, has_wifi=True): ...
    async def start(self, ...hardware pins...): ...

    def _init_segments(self): ...        # canopy.Segment per LED zone
    def _init_patterns(self): ...        # canopy.Pattern per visual state

    def _on_wifi_connected(self): ...
    def _on_mqtt_message(self, topic, msg): ...
    def _handle_remote_event(self, command, data): ...

    def _check_win(self): ...
    def _update_state(self, event, should_broadcast=True): ...

    async def _display_loop(self): ...   # wakes on asyncio.Event
    async def _update_displays(self): ...
    async def _render_loop(self): ...    # fixed 100 ms cadence
```

### Key Design Decisions

**Single `_update_state()` entry point.** All events — hardware callbacks, MQTT, button polling — funnel through one method. Mode transitions and broadcasts happen there.

**`asyncio.Event` for display wakeup.** `_display_loop` sleeps until `_display_event.set()` is called, avoiding unnecessary I2C traffic on idle frames. Encoder changes also set the event (not just mode changes) so the display stays responsive.

**I2C MUX + shared lock.** Where multiple devices share the same I2C address (encoders in word puzzle; RFID readers in artifact puzzle), a single `asyncio.Lock()` prevents concurrent mux port switching. The time puzzle encoders use distinct addresses so no lock is needed.

**`NoMux` wrapper.** The time puzzle's `LargeDisplay` is not behind a mux. `NoMux` (from `i2c_mux`) gives it the same `select()`/`deselect()` interface as mux-backed displays so the `Display` class works unchanged.

**LED render loop at fixed 100 ms.** Display updates are event-driven; LED updates are time-driven for smooth animation regardless of input rate.

**`canopy.Segment` for LED zones.** Each logical LED region gets its own `Segment` so patterns are targeted independently. The artifact puzzle uses a stride-7 layout; the clock face uses pre-built arrays of per-position segments.

**Game master on Puzzle 1.** `BabelTimePuzzle._handle_puzzle_solved()` maps each incoming `*Solved` event to the next `gameUpdate` state string. If this board crashes mid-game the others freeze in their current mode — acceptable given the physical game context.

**CTP pattern strings are placeholders in Puzzle 2.** `babel_artifact_puzzle.py` uses `"CTP-PLACEHOLDER_*"` strings that must be replaced with real canopy tool output before the board is deployed.

---

## File Summary

| File                           | Runs on  | Status          |
|--------------------------------|----------|-----------------|
| `babel_time_puzzle.py`         | ESP #1   | Written          |
| `babel_artifact_puzzle.py`     | ESP #2   | Written (needs real CTP strings + RFID tag UIDs) |
| `babel_constellation_puzzle.py`| ESP #3   | Written          |
| `babel_word_puzzle.py`         | ESP #4   | Written (needs real word lists + winning combo)  |
| `ratlantis_pi/`                | Pi       | To be written    |

Each ESP's `main.py` imports the relevant class and calls `await puzzle.start(...)`.
