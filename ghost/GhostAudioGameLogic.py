import random
import time

from timemachine.Button import GameButtonWithFourLights
from timemachine.Switches import GameThreeWaySwitch, GameTwoWaySwitch
from ratlantis.Switchboard import Switchboard
from ghost.ElevatorButtons import GameElevatorButtons
from ghost.GhostAudioSoundSystem import GhostAudioSoundSystem

EVENT_GHOST_UPDATE = "ghostUpdate"
# EVENT_WRITE_RFID_COMMAND = "writeRfid"
EVENT_SET_RUNNING = "setRunning"
EVENT_SET_FINISHED = "setFinished"
EVENT_RESET_COMMAND = "reset"
LISTENING_MACHINE_ID = "listening"

GAME_MODE_OFF = 0
GAME_MODE_SCANNING = 1
GAME_MODE_READY = 2
GAME_MODE_ROUND_START = 3
GAME_MODE_RUNNING = 4
GAME_MODE_WIN = 5
GAME_MODE_LOSE = 6

GAME_WAIT_TIMEOUT = 20
GAME_STARTUP_TIME = 8
ROUND_TIME = 16
ROUND_START_TIME = 2
LOW_ENERGY_LEVEL_TIME_S = 3
GAME_OVER_TIME = 10
GAME_WIN_TIME = 30
SCANNING_TIME = 10

NUM_OBJECTIVES_NORMAL = 8
NUM_OBJECTIVES_HARD = 12  # Hard mode: 4 rounds of 1, 4 rounds of 2, 4 rounds of 3

OBJECTIVE_NONE = -1
OBJECTIVE_SWITCH_A = 0
OBJECTIVE_SWITCH_B = 1
OBJECTIVE_POWER_SWITCH = 2
OBJECTIVE_RED_BUTTON = 3
OBJECTIVE_GREEN_BUTTON = 4
OBJECTIVE_SWITCHBOARD = 5
OBJECTIVE_ELEVATOR_BUTTONS = 6


class GhostAudioGameLogic(object):
    mode = GAME_MODE_OFF
    current_round = 0
    current_objectives = []  # Changed to array for hard mode
    current_rfid = None
    hard_mode = False  # Hard mode disabled by default (old behavior)

    scanning_end_time = 0
    next_round_start_time = 0
    celebration_end_time = 0
    round_end_time = 0
    game_timeout_time = 0

    playing_running_out_of_time = False

    def __init__(self, green_button: GameButtonWithFourLights, red_button: GameButtonWithFourLights, switch_a: GameTwoWaySwitch, switch_b: GameTwoWaySwitch, power_switch: GameThreeWaySwitch, switchboard: Switchboard, elevator_buttons: GameElevatorButtons, mqtt, sound: GhostAudioSoundSystem, on_change_mode):
        self.green_button = green_button
        self.red_button = red_button
        self.switch_a = switch_a
        self.switch_b = switch_b
        self.power_switch = power_switch
        self.switchboard = switchboard
        self.elevator_buttons = elevator_buttons
        self.mqtt = mqtt
        self.sound = sound
        self.on_change_mode = on_change_mode
        self.sound.play_ambient()

    def _get_num_objectives_for_round(self):
        """Determine how many objectives to have based on hard mode and current round."""
        if not self.hard_mode:
            return 1
        # Hard mode progression:
        # Rounds 1-4: 1 objective at a time
        # Rounds 5-8: 2 objectives at a time
        # Rounds 9-12: 3 objectives at a time
        if self.current_round <= 2:
            return 1
        elif self.current_round <= 5:
            return 2
        elif self.current_round <= 8:
            return 3
        else:
            return 4

    def _get_next_objectives(self):
        """Get the next set of objectives based on hard mode progression."""
        print("Updating Objectives")
        num_objectives = self._get_num_objectives_for_round()
        print(f"Hard mode: {self.hard_mode}, Round: {self.current_round}, Objectives needed: {num_objectives}")
        
        options = [OBJECTIVE_SWITCH_A, OBJECTIVE_SWITCH_B, OBJECTIVE_RED_BUTTON, OBJECTIVE_GREEN_BUTTON, OBJECTIVE_SWITCHBOARD, OBJECTIVE_ELEVATOR_BUTTONS, OBJECTIVE_POWER_SWITCH]
        
        # Filter out objectives that were just completed (except switchboard and elevator buttons can repeat)
        available_options = options.copy()
        for prev_obj in self.current_objectives:
            if prev_obj != OBJECTIVE_SWITCHBOARD and prev_obj != OBJECTIVE_ELEVATOR_BUTTONS:
                available_options = [x for x in available_options if x != prev_obj]
        
        # Select the required number of objectives
        selected_objectives = []
        for _ in range(num_objectives):
            if len(available_options) == 0:
                # If we run out of options, reset to all options
                available_options = options.copy()
            chosen = random.choice(available_options)
            selected_objectives.append(chosen)
            # Remove chosen option (except switchboard and elevator buttons can repeat)
            if chosen != OBJECTIVE_SWITCHBOARD and chosen != OBJECTIVE_ELEVATOR_BUTTONS:
                available_options = [x for x in available_options if x != chosen]
        
        self.current_objectives = selected_objectives
        print(f"New Objectives: {self.current_objectives}")
        
        # Stop any previous objective sounds before starting new ones
        self.sound.stop_all_objective_sounds()
        
        # Set up each objective
        for objective in self.current_objectives:
            if objective == OBJECTIVE_SWITCH_A:
                if self.switch_a.mode == 0:
                    self.sound.play_increase_auraral()
                else:
                    self.sound.play_decrease_auraral()
                self.switch_a.set_desired_mode(not self.switch_a.mode)
            elif objective == OBJECTIVE_SWITCH_B:
                if self.switch_b.mode == 0:
                    self.sound.play_activate_chronometer()
                else:
                    self.sound.play_deactivate_chronometer()
                self.switch_b.set_desired_mode(not self.switch_b.mode)
            elif objective == OBJECTIVE_POWER_SWITCH:
                if self.power_switch.mode == 1:
                    self.power_switch.set_desired_mode(3)
                    self.sound.play_decrease_insulation()
                else:
                    self.power_switch.set_desired_mode(1)
                    self.sound.play_increase_insulation()
            elif objective == OBJECTIVE_RED_BUTTON:
                self.red_button.set_pending()
                self.sound.play_initiate_flux()
            elif objective == OBJECTIVE_GREEN_BUTTON:
                self.green_button.set_pending()
                self.sound.play_engage_numinsity()
            elif objective == OBJECTIVE_SWITCHBOARD:
                self.switchboard.request_new_state()
                self.sound.play_magnetize_matrix()
            elif objective == OBJECTIVE_ELEVATOR_BUTTONS:
                self.elevator_buttons.set_desired_button(random.choice([1, 3, 4, 7]))
                if self.elevator_buttons.desired_button == 7:
                    self.sound.play_increase_accelerator()
                else:
                    self.sound.play_determine_accelerator()

    def _set_party_mode(self):
        self.switchboard.clear()
        self.green_button.set_party_mode()
        self.red_button.set_party_mode()
        self.switch_a.set_party_mode()
        self.switch_b.set_party_mode()
        self.power_switch.set_party_mode()
        self.elevator_buttons.set_party_mode()

    def _turn_off_inputs(self):
        self.green_button.off()
        self.red_button.off()
        self.switch_a.off()
        self.switch_b.off()
        self.power_switch.off()
        self.elevator_buttons.off()
        self.switchboard.clear()

    def start_scanning(self, rfid, hard_mode=False):
        self.current_rfid = rfid
        self.hard_mode = hard_mode
        self._change_game_mode(GAME_MODE_SCANNING)

    def _change_game_mode(self, new_mode):
        old_mode = self.mode
        self.mode = new_mode
        print("updating game mode from", old_mode, "to", new_mode)

        if new_mode == GAME_MODE_OFF:
            print("Game is off")
            self._turn_off_inputs()
            self.sound.play_ambient()
            self.switchboard.do_ambient()
            self.game_timeout_time = 0
            self.current_rfid = None
            self.mqtt.queue_in_batch_publish({
                "event": EVENT_GHOST_UPDATE,
                "id": LISTENING_MACHINE_ID,
                "command": EVENT_RESET_COMMAND,
            })
        elif new_mode == GAME_MODE_SCANNING:
            print("Game Scanning")
            self._set_party_mode()
            self.scanning_end_time = time.time() + SCANNING_TIME
            self.sound.play_scanning()
            self.mqtt.queue_in_batch_publish({
                "event": EVENT_GHOST_UPDATE,
                "reader": LISTENING_MACHINE_ID,
                "id": LISTENING_MACHINE_ID,
                "command": EVENT_SET_RUNNING,
            })
        elif new_mode == GAME_MODE_READY:
            print("Game Ready")
            self.current_round = 0
            self.current_objectives = []  # Reset objectives
            self.next_round_start_time = 0
            self._turn_off_inputs()
            self.sound.play_intro_scan()
            self.green_button.set_pending()
            self.game_timeout_time = time.time() + GAME_WAIT_TIMEOUT
        elif new_mode == GAME_MODE_ROUND_START:
            if self.current_round > 0:
                self.sound.play_objective_completed()
            self.sound.stop_running_out_of_time()
            self.current_round += 1
            print("Game Starting Objective", self.current_round)
            self.next_round_start_time = time.time() + ROUND_START_TIME
            self._turn_off_inputs()
            self.playing_running_out_of_time = False
            self.game_round_length = ROUND_TIME - int(self.current_round / 2) 
            self.game_timeout_time = 0
            self.sound.play_game_backround()
        elif new_mode == GAME_MODE_RUNNING:
            print("Game Running")
            self._get_next_objectives()
            self.round_end_time = time.time() + self.game_round_length
        elif new_mode == GAME_MODE_WIN:
            print("Game Win!")
            self.sound.stop_running_out_of_time()

            def reset():
                self._change_game_mode(GAME_MODE_OFF)

            def play_put_back_headphones():
                self.sound.play_put_back_headphones()

            def play_story():
                self.sound.play_ghost_story(self.current_rfid)

            def play_story_intro_sounds():
                self.sound.play_story_intro_sounds()

            self.sound.play_you_win()
            self.sound.set_next_event_callbacks([play_story_intro_sounds, play_story, play_put_back_headphones, reset])
            self.celebration_end_time = time.time() + GAME_WIN_TIME
            self._set_party_mode()
            self.mqtt.queue_in_batch_publish({
                "event": EVENT_GHOST_UPDATE,
                "id": LISTENING_MACHINE_ID,
                "command": EVENT_SET_FINISHED,
            })
            # PLAY THE GHOST AUDIO
        elif new_mode == GAME_MODE_LOSE:
            print("Game Lose!")
            self.sound.stop_running_out_of_time()
            self.sound.play_game_over()

            def reset():
                self._change_game_mode(GAME_MODE_OFF)
            
            self.sound.set_next_event_callbacks([reset])
            self.current_rfid = None
            self.celebration_end_time = time.time() + GAME_OVER_TIME
            self._set_party_mode()
            self.mqtt.queue_in_batch_publish({
                "event": EVENT_GHOST_UPDATE,
                "id": LISTENING_MACHINE_ID,
                "command": EVENT_SET_FINISHED,
            })
        self.on_change_mode(self.mode)

    def update(self):
        now = time.time()
        if self.mode == GAME_MODE_LOSE:
            if now >= self.celebration_end_time:
                self._change_game_mode(GAME_MODE_OFF)
                return
        elif self.mode == GAME_MODE_WIN:
            # if not self.sound.is_still_playing(1):
            #     self.celebration_end_time = 0
            #     # self._change_game_mode(GAME_MODE_OFF)
            return
        elif self.mode == GAME_MODE_SCANNING:
            if now >= self.scanning_end_time:
                print("Finished scanning")
                self._change_game_mode(GAME_MODE_READY)
                return
        elif self.mode == GAME_MODE_ROUND_START:
            if now >= self.next_round_start_time:
                print("Finished waiting for next round")
                self._change_game_mode(GAME_MODE_RUNNING)
                return
        elif self.mode == GAME_MODE_READY:
            if self.green_button.completed and self.next_round_start_time == 0:
                print("Starting game sequence!")
                self.next_round_start_time = now + GAME_STARTUP_TIME
                self.game_timeout_time = 0
                self.sound.play_startup()
                self._change_game_mode(GAME_MODE_ROUND_START)
                return
            if self.next_round_start_time > 0 and now >= self.next_round_start_time:
                print("Starting Game!")
                self._change_game_mode(GAME_MODE_ROUND_START)
                return
            if self.game_timeout_time > 0 and now >= self.game_timeout_time:
                print("Game timed out")
                self._change_game_mode(GAME_MODE_OFF)
        elif self.mode == GAME_MODE_RUNNING:
            if now >= self.round_end_time:
                print("Ran out of time")
                self._change_game_mode(GAME_MODE_LOSE)
                return
            if now >= self.round_end_time - (self.game_round_length / 2) and not self.playing_running_out_of_time:
                self.playing_running_out_of_time = True
                self.sound.play_running_out_of_time()

            # Check if all objectives are completed
            is_objective_completed = True
            for objective in self.current_objectives:
                objective_done = False
                if objective == OBJECTIVE_SWITCH_A:
                    if self.switch_a.mode == self.switch_a.desired_mode:
                        objective_done = True
                elif objective == OBJECTIVE_SWITCH_B:
                    if self.switch_b.mode == self.switch_b.desired_mode:
                        objective_done = True
                elif objective == OBJECTIVE_POWER_SWITCH:
                    if self.power_switch.mode == self.power_switch.desired_mode:
                        objective_done = True
                elif objective == OBJECTIVE_RED_BUTTON:
                    if self.red_button.completed:
                        objective_done = True
                elif objective == OBJECTIVE_GREEN_BUTTON:
                    if self.green_button.completed:
                        objective_done = True
                elif objective == OBJECTIVE_SWITCHBOARD:
                    if self.switchboard.is_completed():
                        objective_done = True
                elif objective == OBJECTIVE_ELEVATOR_BUTTONS:
                    if self.elevator_buttons.completed:
                        objective_done = True
                
                if not objective_done:
                    is_objective_completed = False
                    break
            
            if is_objective_completed:
                print("Objective completed")
                num_objectives = NUM_OBJECTIVES_HARD if self.hard_mode else NUM_OBJECTIVES_NORMAL
                if self.current_round == num_objectives:
                    self._change_game_mode(GAME_MODE_WIN)
                else:
                    self._change_game_mode(GAME_MODE_ROUND_START)
