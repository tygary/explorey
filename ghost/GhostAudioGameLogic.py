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
ROUND_TIME = 10
ROUND_START_TIME = 2
LOW_ENERGY_LEVEL_TIME_S = 3
GAME_OVER_TIME = 10
GAME_WIN_TIME = 55
SCANNING_TIME = 10

NUM_OBJECTIVES = 8

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
    current_objective = OBJECTIVE_NONE
    current_rfid = None

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

    def _get_next_objective(self):
        print("Updating Objectives")
        options = [OBJECTIVE_SWITCH_A, OBJECTIVE_SWITCH_B, OBJECTIVE_POWER_SWITCH, OBJECTIVE_RED_BUTTON, OBJECTIVE_GREEN_BUTTON, OBJECTIVE_SWITCHBOARD, OBJECTIVE_ELEVATOR_BUTTONS]
        if self.current_objective != OBJECTIVE_SWITCHBOARD and self.current_objective != OBJECTIVE_ELEVATOR_BUTTONS:
            options = [x for x in options if x != self.current_objective]
        self.current_objective = random.choice(options)
        if self.current_objective == OBJECTIVE_SWITCH_A:
            if self.switch_a.mode == 0:
                self.sound.play_increase_auraral()
            else:
                self.sound.play_decrease_auraral()
            self.switch_a.set_desired_mode(not self.switch_a.mode)
        if self.current_objective == OBJECTIVE_SWITCH_B:
            if self.switch_b.mode == 0:
                self.sound.play_activate_chronometer()
            else:
                self.sound.play_deactivate_chronometer()
            self.switch_b.set_desired_mode(not self.switch_b.mode)
        if self.current_objective == OBJECTIVE_POWER_SWITCH:
            if self.power_switch.mode == 1:
                self.power_switch.set_desired_mode(3)
                self.sound.play_decrease_insulation()
            else:
                self.power_switch.set_desired_mode(1)
                self.sound.play_increase_insulation()
        if self.current_objective == OBJECTIVE_RED_BUTTON:
            self.red_button.set_pending()
            self.sound.play_initiate_flux()
        if self.current_objective == OBJECTIVE_GREEN_BUTTON:
            self.green_button.set_pending()
            self.sound.play_engage_numinsity()
        if self.current_objective == OBJECTIVE_SWITCHBOARD:
            self.switchboard.request_new_state()
            self.sound.play_magnetize_matrix()
            # self.sound.play_pending_switchboard()
        if self.current_objective == OBJECTIVE_ELEVATOR_BUTTONS:
            self.elevator_buttons.set_desired_button(random.choice([1, 3, 4, 7]))
            if self.elevator_buttons.desired_button == 7:
                self.sound.play_increase_accelerator()
            else:
                self.sound.play_determine_accelerator()
        print("New Objective:", self.current_objective)

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

    def start_scanning(self, rfid):
        self.current_rfid = rfid
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
            self._turn_off_inputs()
            self.sound.play_intro_scan()
            self.green_button.set_pending()
            self.game_timeout_time = time.time() + GAME_WAIT_TIMEOUT
        elif new_mode == GAME_MODE_ROUND_START:
            if self.current_round == 0:
                self.sound.play_startup()
            else:
                self.sound.play_objective_completed()
            self.sound.stop_running_out_of_time()
            self.current_round += 1
            print("Game Starting Objective", self.current_round)
            self.next_round_start_time = time.time() + ROUND_START_TIME
            self._turn_off_inputs()
            self.playing_running_out_of_time = False
            self.game_timeout_time = 0
            self.sound.play_game_backround()
        elif new_mode == GAME_MODE_RUNNING:
            print("Game Running")
            self._get_next_objective()
            self.round_end_time = time.time() + ROUND_TIME
        elif new_mode == GAME_MODE_WIN:
            print("Game Win!")
            self.sound.stop_running_out_of_time()
            self.sound.play_you_win()
            self.sound.queue_ghost_story(self.current_rfid)
            # self.celebration_end_time = time.time() + GAME_WIN_TIME
            self._set_party_mode()
            self.current_rfid = None
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
            self.sound.queue_put_back_headphones()
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
            if not self.sound.is_still_playing(1):
                self._change_game_mode(GAME_MODE_OFF)
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
            if self.green_button.completed:
                print("Starting Game!")
                self._change_game_mode(GAME_MODE_ROUND_START)
                return
            if now >= self.game_timeout_time:
                print("Game timed out")
                self._change_game_mode(GAME_MODE_OFF)
        elif self.mode == GAME_MODE_RUNNING:
            if now >= self.round_end_time:
                print("Ran out of time")
                self._change_game_mode(GAME_MODE_LOSE)
                return
            if now >= self.round_end_time - LOW_ENERGY_LEVEL_TIME_S and not self.playing_running_out_of_time:
                print("Running low on time")
                # self.sound.play_running_out_of_time()
                self.playing_running_out_of_time = True
                self.sound.play_running_out_of_time()

            is_objective_completed = True
            if self.current_objective == OBJECTIVE_SWITCH_A:
                if self.switch_a.mode != self.switch_a.desired_mode:
                    is_objective_completed = False
            if self.current_objective == OBJECTIVE_SWITCH_B:
                if self.switch_b.mode != self.switch_b.desired_mode:
                    is_objective_completed = False
            if self.current_objective == OBJECTIVE_POWER_SWITCH:
                if self.power_switch.mode != self.power_switch.desired_mode:
                    is_objective_completed = False
            if self.current_objective == OBJECTIVE_RED_BUTTON:
                if not self.red_button.completed:
                    is_objective_completed = False
            if self.current_objective == OBJECTIVE_GREEN_BUTTON:
                if not self.green_button.completed:
                    is_objective_completed = False
            if self.current_objective == OBJECTIVE_SWITCHBOARD:
                if not self.switchboard.is_completed():
                    is_objective_completed = False
            if self.current_objective == OBJECTIVE_ELEVATOR_BUTTONS:
                if not self.elevator_buttons.completed:
                    is_objective_completed = False
            if is_objective_completed:
                print("Objective completed")
                if self.current_round == NUM_OBJECTIVES:
                    self._change_game_mode(GAME_MODE_WIN)
                else:
                    self._change_game_mode(GAME_MODE_ROUND_START)
