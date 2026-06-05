# Ratlantis Game — Implementation Plan

## Overview

Two physical puzzle boxes — **Pigeon** and **Elephant** — each contain the same four puzzles. Both boxes must solve their puzzles simultaneously; the game advances to the next phase only when both boxes have completed the current one.

Five device types: four ESP boards per box (eight total), and a Raspberry Pi. The **Raspberry Pi is the game master** — it owns global state, coordinates phase transitions, and responds to any puzzle reboot with a `gameUpdate` that restores that puzzle to the correct state. All devices communicate over MQTT on the shared topic `ratlantis`.

Each puzzle class takes a `pigeon` parameter (`True` for the pigeon box, `False` for the elephant box). This flag controls which image assets are used, which MQTT box identifier is embedded in outgoing messages, and any behaviour that differs between the two boxes.

**Image naming convention:**
- Pigeon box: `images/p_<word>.bin`
- Elephant box: `images/E_<word>.bin`

---

## Game Flow

```
GAME_INIT           → (both boxes hold button simultaneously)  → PUZZLE_1_ACTIVE
PUZZLE_1_ACTIVE     → (pigeon matches elephant's chosen time)  → PUZZLE_2_ACTIVE
PUZZLE_2_ACTIVE     → (both boxes have all artifacts correct)  → PUZZLE_3_ACTIVE
PUZZLE_3_ACTIVE     → (all 6 constellation pairs correct)      → PUZZLE_4_ACTIVE
PUZZLE_4_ACTIVE     → (all 6 words correct across both boxes)  → GAME_COMPLETE
```

Reset: hold the button on either box's Time Puzzle for 5 seconds → `GAME_INIT` broadcast from Pi.

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

Every message includes a `box` field: `"pigeon"` or `"elephant"`. The `id` field is the puzzle name (e.g. `"time_puzzle"`). The Pi uses both fields to route and track state.

---

### ESP → Pi (and broadcast to all)

#### finishedBoot
Sent by any puzzle immediately after WiFi and MQTT connect. The Pi responds with the appropriate `gameUpdate` to restore state.

```json
{ "event": "finishedBoot", "id": "time_puzzle", "box": "pigeon" }
```

#### holdButton (Time Puzzle only)
Sent when the button is held ≥ 1 s. Pi tracks whether both boxes are holding simultaneously.

```json
{ "event": "holdButton", "id": "time_puzzle", "box": "pigeon", "holding": true }
{ "event": "holdButton", "id": "time_puzzle", "box": "pigeon", "holding": false }
```

#### timePuzzleSolved (Pigeon only)
Sent when the pigeon box sets the correct time and presses the button.

```json
{ "event": "timePuzzleSolved", "id": "time_puzzle", "box": "pigeon" }
```

#### artifactPuzzleSolved
Sent when all three slots on one box are correct.

```json
{ "event": "artifactPuzzleSolved", "id": "artifact_puzzle", "box": "pigeon" }
```

#### constellationUpdate
Sent on every cable connection change while playing.

```json
{ "event": "constellationUpdate", "id": "constellation_puzzle", "box": "pigeon",
  "connections": { "cable1": "<plug_pin>", "cable2": null, "cable3": "<plug_pin>" } }
```

#### constellationPuzzleSolved
Sent when all three cables on one box are correct (Pi still waits for both).

```json
{ "event": "constellationPuzzleSolved", "id": "constellation_puzzle", "box": "pigeon" }
```

#### wordKnobChanged
Sent when a knob turns. `dial` is the global dial index (0–2 pigeon, 3–5 elephant). Pi rebroadcasts this to all devices so both boxes update their displays.

```json
{ "event": "wordKnobChanged", "id": "babel_word_puzzle", "box": "pigeon",
  "dial": 1, "value": 4 }
```

---

### Pi → All (game master commands)

#### gameUpdate
The Pi's primary outgoing message. Sent to advance game state and to restore any rebooted puzzle. Includes the full current state so every puzzle can self-correct without extra round-trips.

```json
{
  "event": "gameUpdate",
  "state": "puzzle1Active",
  "time_target": { "hour": 3, "minute": 7 },
  "constellation_connections": {
    "pigeon": { "cable1": null, "cable2": null, "cable3": null },
    "elephant": { "cable1": null, "cable2": null, "cable3": null }
  },
  "word_selections": [0, 0, 0, 0, 0, 0]
}
```

State strings: `"init"`, `"puzzle1Active"`, `"puzzle2Active"`, `"puzzle3Active"`, `"puzzle4Active"`, `"gameComplete"`

Fields present in each state:

| State          | Extra fields present                                             |
|----------------|------------------------------------------------------------------|
| `init`         | —                                                                |
| `puzzle1Active`| `time_target` (null until elephant has chosen, then hour+minute) |
| `puzzle2Active`| —                                                                |
| `puzzle3Active`| `constellation_connections`                                      |
| `puzzle4Active`| `word_selections` (array of 6 ints)                              |
| `gameComplete` | —                                                                |

#### wordKnobChanged (relay)
The Pi rebroadcasts this verbatim so both boxes update their display for that dial.

---

## Puzzle 1 — Time Puzzle

**File:** `babel_time_puzzle.py` | **Class:** `BabelTimePuzzle` | **Param:** `pigeon=True/False`

### Hardware

| Component               | Pigeon                                          | Elephant                              |
|-------------------------|-------------------------------------------------|---------------------------------------|
| Start/reset button      | `fern.D1`, active low, PULL_UP                  | Same                                  |
| LargeDisplay            | Direct I2C, addr `0x3C` via `NoMux`             | Same                                  |
| RotaryEncoder (hour)    | Direct I2C, addr `0x36`                         | **Not present**                       |
| RotaryEncoder (minute)  | Direct I2C, addr `0x37`                         | **Not present**                       |
| LED strip               | `LED1_DATA`, 73 LEDs total                      | Same                                  |

### Behaviour Differences

**Elephant (`pigeon=False`):**
- On entering `MODE_PLAYING`: randomly picks `hour` (1–12) and `minute` (0–11) and publishes `timeChosen` to Pi.
- Displays the chosen time on its own clock face LEDs and LargeDisplay.
- Has no rotary encoders and no win condition — it waits for `timePuzzleSolved` from the pigeon box.
- The Pi stores the chosen time in state and includes it in future `gameUpdate` messages.

**Pigeon (`pigeon=True`):**
- Has rotary encoders. User sets hour and minute.
- Listens for `time_target` in `gameUpdate` to know the target time. Displays the target on its LargeDisplay alongside its own clock face.
- Win: `hour_position == time_target.hour and minute_position == time_target.minute`. Triggered by button press. Broadcasts `timePuzzleSolved`.

### timeChosen Message (Elephant → Pi)

```json
{ "event": "timeChosen", "id": "time_puzzle", "box": "elephant",
  "hour": 3, "minute": 7 }
```

Pi stores `time_target = {hour, minute}` and rebroadcasts a `gameUpdate` with `time_target` so the pigeon box and any rebooted device gets it.

### Button Behaviour

Polled every 50 ms. Active low.

- **Both boxes, hold ≥ 5 s:** Pi receives `holdButton` from each; when both are holding simultaneously (within 2 s of each other), Pi broadcasts `gameUpdate` with `state: "puzzle1Active"`. Either box holding alone resets to `GAME_INIT`.
- **Pigeon, short press, playing:** Checks win. On win → broadcasts `timePuzzleSolved`.

### LED Layout (73 LEDs)

Same layout as before; elephant box shows the chosen time as a static display on its clock face.

### Display

Both boxes use `LargeDisplay` to show two 64×64 pigeon or elephant symbol images side by side. Images at `images/pigeon_N.bin` (pigeon box) or `images/E_N.bin` (elephant box) where N is 1–12.

---

## Puzzle 2 — Artifact Puzzle

**File:** `babel_artifact_puzzle.py` | **Class:** `BabelArtifactPuzzle` | **Param:** `pigeon=True/False`

### Behaviour

Both boxes operate identically to the current design. Each box independently scans three RFID slots. When all three slots on a box are correct, that box broadcasts `artifactPuzzleSolved`. The Pi advances to `puzzle3Active` only when **both** boxes have sent `artifactPuzzleSolved`.

### Image Assets

Pigeon box uses `images/p_ship.bin`, `images/p_crab.bin`, `images/p_hole.bin`. Elephant box uses `images/E_ship.bin`, `images/E_crab.bin`, `images/E_hole.bin` (or equivalent elephant-set images). The `pigeon` parameter selects the correct path prefix.

### State Recovery

On `finishedBoot`, the Pi responds with `gameUpdate`. If state is `puzzle2Active`, the box enters `MODE_PLAYING` and starts scanning. If state is later (puzzle already solved), it enters `MODE_COMPLETED`.

---

## Puzzle 3 — Constellation Puzzle

**File:** `babel_constellation_puzzle.py` | **Class:** `BabelConstellationPuzzle` | **Param:** `pigeon=True/False`

### Behaviour

Both boxes operate independently. Each has 3 cables and 4 plug sockets. When a connection changes, the box broadcasts `constellationUpdate` including the `box` field. The Pi tracks all 6 connections (3 from each box) and advances to `puzzle4Active` when all 6 are simultaneously correct.

The ESP puzzle itself still detects and broadcasts its own 3-cable win (`constellationPuzzleSolved`), but the Pi makes the final call on advancing.

### Correct Connections

Each box has its own `CORRECT_CONNECTIONS` dict (same physical definition, same logical symbol pairs). The Pi mirrors the correct mapping for both boxes to check win state.

### constellationUpdate Payload

```json
{ "event": "constellationUpdate", "id": "constellation_puzzle", "box": "pigeon",
  "connections": { "cable1": 26, "cable2": null, "cable3": 28 } }
```

### State Recovery

On `finishedBoot` while state is `puzzle3Active`, the Pi's `gameUpdate` includes the current `constellation_connections` for both boxes. Each box restores its own `_connections` dict from `connections[box]` and re-renders.

---

## Puzzle 4 — Word Puzzle

**File:** `babel_word_puzzle.py` | **Class:** `BabelWordPuzzle` | **Param:** `pigeon=True/False`

### Layout

Each physical box has 6 displays. The Pigeon box controls **dials 0–2** (words 0–2); the Elephant box controls **dials 3–5** (words 3–5). Both boxes show all 6 displays simultaneously.

| Display index | Controlled by   | Pigeon box shows    | Elephant box shows  |
|---------------|-----------------|---------------------|---------------------|
| 0             | Pigeon dial 0   | `p_<word0>.bin`     | `E_<word0>.bin`     |
| 1             | Pigeon dial 1   | `p_<word1>.bin`     | `E_<word1>.bin`     |
| 2             | Pigeon dial 2   | `p_<word2>.bin`     | `E_<word2>.bin`     |
| 3             | Elephant dial 3 | `p_<word3>.bin`     | `E_<word3>.bin`     |
| 4             | Elephant dial 4 | `p_<word4>.bin`     | `E_<word4>.bin`     |
| 5             | Elephant dial 5 | `p_<word5>.bin`     | `E_<word5>.bin`     |

### Cross-Box Knob Synchronisation

When any dial turns, the local puzzle broadcasts `wordKnobChanged` to the Pi. The Pi updates `word_selections[dial]` and rebroadcasts `wordKnobChanged` to all devices. Both boxes receive it and update the appropriate display (using their own image set based on `pigeon`).

This means both boxes always show the same word indices; they just render them in their own visual language.

### Win Condition

Pi checks `word_selections == WINNING_COMBO` after every `wordKnobChanged`. When matched, Pi broadcasts `gameUpdate` with `state: "gameComplete"`.

### State Recovery

On `finishedBoot` while state is `puzzle4Active`, the Pi includes `word_selections` in `gameUpdate`. Each box restores all six display positions and re-renders.

### SYMBOLS List

Same symbol list for both boxes, but path prefix differs by `pigeon`:
- Pigeon: `images/p_<word>.bin`
- Elephant: `images/E_<word>.bin`

`WINNING_COMBO` is a 6-tuple, e.g. `(2, 2, 2, 1, 1, 1)`, set to the actual puzzle answer before deployment.

---

## Raspberry Pi — Game Master

The Pi has four responsibilities: MQTT broker, global state management, constellation LED rendering, and the win sequence. It is the single source of truth for game phase.

### MQTT Broker

Run **Mosquitto** on the Pi. All nine devices (8 ESPs + Pi client) connect to it.

### State Object

```python
state = {
    "phase": "init",  # init | puzzle1Active | puzzle2Active | puzzle3Active | puzzle4Active | gameComplete

    # Per-box puzzle completion flags
    "completed": {
        "pigeon":   {"time": False, "artifact": False, "constellation": False, "word": False},
        "elephant": {"time": False, "artifact": False, "constellation": False, "word": False},
    },

    # Time puzzle target (set when elephant chooses a time)
    "time_target": None,  # None | {"hour": int, "minute": int}

    # Constellation connections (updated on every constellationUpdate)
    "constellation_connections": {
        "pigeon":   {"cable1": None, "cable2": None, "cable3": None},
        "elephant": {"cable1": None, "cable2": None, "cable3": None},
    },

    # Correct constellation answers (mirrored from ESP config)
    "constellation_correct": {
        "pigeon":   {"cable1": D4, "cable2": D6, "cable3": D5},
        "elephant": {"cable1": D4, "cable2": D6, "cable3": D5},
    },

    # Word puzzle dial positions (6 total; pigeon owns 0-2, elephant owns 3-5)
    "word_selections": [0, 0, 0, 0, 0, 0],

    # Winning word combination
    "word_winning_combo": [2, 2, 2, 1, 1, 1],  # set to actual answer

    # Button hold tracking for game start
    "holding": {"pigeon": False, "elephant": False},
    "hold_start": {"pigeon": None, "elephant": None},
}
```

### Event Handlers

#### `finishedBoot`
Respond with a `gameUpdate` restoring the puzzle to its correct state.

```python
def on_finished_boot(box, puzzle_id):
    send_game_update()   # includes current phase + all relevant state fields
```

#### `holdButton`
Track which boxes are currently holding. If both are holding within 2 seconds of each other, transition `init → puzzle1Active` and send `gameUpdate`.

```python
def on_hold_button(box, holding):
    state["holding"][box] = holding
    state["hold_start"][box] = time.time() if holding else None
    if all(state["holding"].values()):
        starts = list(state["hold_start"].values())
        if abs(starts[0] - starts[1]) <= 2.0:
            transition_to("puzzle1Active")
    elif state["phase"] == "init":
        pass  # one box released, stay in init
```

#### `timeChosen`
Store the target time and relay it to all devices via `gameUpdate`.

```python
def on_time_chosen(hour, minute):
    state["time_target"] = {"hour": hour, "minute": minute}
    send_game_update()  # rebroadcast with time_target so pigeon box gets it
```

#### `timePuzzleSolved`
Mark pigeon time as complete. Elephant time is implicitly complete (it chose the time). Advance if both done.

```python
def on_time_puzzle_solved(box):
    state["completed"][box]["time"] = True
    state["completed"]["elephant"]["time"] = True  # elephant always complete once it chose
    maybe_advance()
```

#### `artifactPuzzleSolved`

```python
def on_artifact_puzzle_solved(box):
    state["completed"][box]["artifact"] = True
    maybe_advance()
```

#### `constellationUpdate`
Update tracked connections. Check if all 6 are simultaneously correct.

```python
def on_constellation_update(box, connections):
    state["constellation_connections"][box] = connections
    # relay to LED renderer
    render_constellation_leds()
    # check win: all 6 connections match correct
    if all_constellations_correct():
        state["completed"]["pigeon"]["constellation"] = True
        state["completed"]["elephant"]["constellation"] = True
        maybe_advance()
```

#### `constellationPuzzleSolved`
Ignored for phase advancement — Pi uses `constellationUpdate` to check all 6. This event is still useful for local LED celebration on the ESP.

#### `wordKnobChanged`
Update state and relay to all devices. Check win.

```python
def on_word_knob_changed(dial, value):
    state["word_selections"][dial] = value
    relay({"event": "wordKnobChanged", "dial": dial, "value": value})
    if state["word_selections"] == state["word_winning_combo"]:
        transition_to("gameComplete")
```

### `maybe_advance()`

Checks whether both boxes have completed the current phase and transitions to the next:

```python
PHASE_ORDER = ["puzzle1Active", "puzzle2Active", "puzzle3Active", "puzzle4Active", "gameComplete"]
PHASE_KEY   = {"puzzle1Active": "time", "puzzle2Active": "artifact",
               "puzzle3Active": "constellation", "puzzle4Active": "word"}

def maybe_advance():
    key = PHASE_KEY.get(state["phase"])
    if key and all(state["completed"][b][key] for b in ("pigeon", "elephant")):
        next_phase = PHASE_ORDER[PHASE_ORDER.index(state["phase"]) + 1]
        transition_to(next_phase)

def transition_to(phase):
    state["phase"] = phase
    send_game_update()
    if phase == "gameComplete":
        run_win_sequence()
```

### `send_game_update()`

Broadcasts a single `gameUpdate` message with all state fields every ESP might need:

```python
def send_game_update():
    msg = {
        "event": "gameUpdate",
        "state": state["phase"],
        "time_target": state["time_target"],
        "constellation_connections": state["constellation_connections"],
        "word_selections": state["word_selections"],
    }
    mqtt_client.publish("ratlantis", json.dumps(msg))
```

### Constellation LED Rendering

Same as before: Pi controls an LED strip representing the 6 constellation stations (3 per box). On `constellationUpdate`, compare each cable→plug pair against the correct mapping; illuminate correctly-connected constellations with a solved pattern.

### Win Sequence

On `gameComplete`:
1. Run celebration animation across all Pi-controlled LEDs.
2. Trigger relay/servo to open the secret box.

### Pi Software Structure

```
ratlantis_pi/
├── main.py                  # entry point, starts broker client + tasks
├── game_state.py            # state dict, transition logic, maybe_advance()
├── mqtt_client.py           # wraps paho-mqtt, dispatches to handlers
├── event_handlers.py        # one function per incoming event type
├── constellation_leds.py    # LED strip rendering for constellation puzzle
├── win_sequence.py          # celebration lights + box trigger
└── config.py                # MQTT host, pin numbers, correct connection maps, winning combo
```

---

## Code Architecture (ESP Boards)

All puzzle classes share the same structure and accept a `pigeon` boolean:

```python
class Babel<PuzzleName>:
    current_mode = MODE_INITIALIZING

    def __init__(self, name, pigeon=True, has_wifi=True): ...
    async def start(self, ...hardware pins...): ...

    def _image_path(self, word):
        prefix = "p" if self.pigeon else "E"
        return "images/{}_{}.bin".format(prefix, word)

    def _on_wifi_connected(self): ...
    def _on_mqtt_message(self, topic, msg): ...
    def _handle_game_update(self, data): ...  # restores full state from Pi payload

    def _check_win(self): ...
    def _update_state(self, event, **kwargs): ...

    async def _display_loop(self): ...
    async def _update_displays(self): ...
    async def _render_loop(self): ...
```

### Key Design Decisions

**Pi as game master.** No ESP acts as game master. The Pi owns phase transitions. Removing the time puzzle's old game-master role eliminates the single point of failure that was the most complex puzzle.

**`finishedBoot` → `gameUpdate` recovery.** Any ESP that reboots mid-game immediately signals the Pi. The Pi responds with the full state. Each puzzle's `_handle_game_update()` reads the relevant fields and enters the correct mode, restoring display and LED state. No puzzle needs to remember anything across reboots.

**`box` field on all outgoing messages.** Every ESP message includes `"box": "pigeon"` or `"box": "elephant"`. The Pi uses this to route and track per-box completion independently.

**`wordKnobChanged` relay via Pi.** Knob events go ESP → Pi → all ESPs. The Pi is the relay and the win checker. Both boxes always show consistent word displays because they both receive the same relay.

**`pigeon` parameter selects image prefix and encoder presence.** The elephant Time Puzzle skips encoder initialisation entirely. The Word Puzzle uses `pigeon` to determine which dial range to claim (0–2 vs 3–5) and which image prefix to load.

**Hold detection for game start.** The Pi detects simultaneous holds via timestamps. ESPs just report `holdButton: true/false`. This avoids timing-sensitive logic on the constrained ESP.

**`asyncio.Event` for display wakeup, 100 ms render loop for LEDs.** Same as before.

**I2C MUX + shared lock** where multiple devices share an address. Same as before.

---

## File Summary

| File                           | Runs on       | Status                                                                  |
|--------------------------------|---------------|-------------------------------------------------------------------------|
| `babel_time_puzzle.py`         | ESP #1 ×2     | Needs pigeon param, elephant-branch (no encoders, random time choice)   |
| `babel_artifact_puzzle.py`     | ESP #2 ×2     | Needs pigeon param, image path prefix, real RFID UIDs                   |
| `babel_constellation_puzzle.py`| ESP #3 ×2     | Needs pigeon param, box field in MQTT, Pi handles 6-way win             |
| `babel_word_puzzle.py`         | ESP #4 ×2     | Needs pigeon param, dial-range split, cross-box relay via Pi            |
| `ratlantis_pi/`                | Pi            | To be written — game master, state, LED renderer, win sequence          |

Each ESP's `main.py` imports the relevant class and calls `await puzzle.start(pigeon=True/False, ...)`.
