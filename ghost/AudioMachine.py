import json
import random
import time
import RPi.GPIO as GPIO

from lighting.PixelControl import PixelControl
from lighting.Colors import Colors
from lighting.routines import Routines
from mqtt.MqttClient import MqttClient

from ratlantis.Switchboard import Switchboard
from timemachine.Switches import GameThreeWaySwitch, GameTwoWaySwitch
from timemachine.Button import GameButtonWithFourLights
from ghost.ElevatorButtons import GameElevatorButtons

from ghost.GhostAudioSoundSystem import GhostAudioSoundSystem
import ghost.GhostAudioGameLogic as game

EVENT_CARD_FOUND = "cardFound"
EVENT_CARD_REMOVED = "cardRemoved"
EVENT_FINISHED_BOOT = "finishedBoot"
EVENT_GHOST_UPDATE = "ghostUpdate"
EVENT_RESET_COMMAND = "reset"
# EVENT_OPEN_DOOR_COMMAND = "openDoor"
# EVENT_WRITE_RFID_COMMAND = "writeRfid"
EVENT_SET_RUNNING = "setRunning"
EVENT_SET_FINISHED = "setFinished"

BUTTON_PIN = 1

TIME_BEFORE_READY_TO_PRINT = 5

SWITCHBOARD_PINS = [16, 13, 25, 24]
RED_BUTTON_PIN = 17
GREEN_BUTTON_PIN = 4
SWITCH_A_PIN = 19
SWITCH_B_PIN = 20
POWER_SWITCH_A_PIN = 5
POWER_SWITCH_B_PIN = 6
ELEVATOR_BUTTONS_PINS = [18, 27, 22, 23]

SWITCHBOARD_PIXELS = [4, 3, 2, 1, 8, 9, 10, 11]
RED_BUTTON_PIXELS = [34, 35, 36, 37]
GREEN_BUTTON_PIXELS = [38, 39, 40, 41]
SWITCH_A_PIXEL_LEFT = 61
SWITCH_A_PIXEL_RIGHT = 62
SWITCH_B_PIXEL_LEFT = 63
SWITCH_B_PIXEL_RIGHT = 64
POWER_SWITCH_TOP_PIXELS = [32, 33]
POWER_SWITCH_BOTTOM_PIXELS = [28, 29]
ELEVATOR_BUTTONS_PIXELS = [48, 49, 50, 51, 52, 53, 54, 55]

SWITCHBOARD_DECO_PIXELS = [16, 17, 18, 19, 20, 21, 22, 23]
HEADPHONE_DECO_PIXELS_TOP = [69, 70, 71, 72, 73, 74, 75, 76]
HEADPHONE_DECO_PIXELS_BOTTOM = [80, 81, 82, 83, 84, 85, 86, 87]
PEDESTAL_DECO_PIXELS = list(range(88, 104))


class AudioMachine(object):
    id = "listening"
    current_rfid = None
    next_event_time = 0

    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        self.pixels = PixelControl(700, led_brightness=180, led_pin=21)
        self.mqtt = MqttClient()
        self.sound = GhostAudioSoundSystem()

        self.switchboard = Switchboard(self.pixels, [4, 3, 2, 1, 8, 9, 10, 11], SWITCHBOARD_PINS)
        self.green_button = GameButtonWithFourLights(self.pixels, GREEN_BUTTON_PIN, GREEN_BUTTON_PIXELS, self.green_button_pressed)
        self.red_button = GameButtonWithFourLights(self.pixels, RED_BUTTON_PIN, RED_BUTTON_PIXELS, self.red_button_pressed)
        self.switch_a = GameTwoWaySwitch(self.pixels, SWITCH_A_PIN, SWITCH_A_PIXEL_LEFT, SWITCH_A_PIXEL_RIGHT, self.switch_a_toggled)
        self.switch_b = GameTwoWaySwitch(self.pixels, SWITCH_B_PIN, SWITCH_B_PIXEL_LEFT, SWITCH_B_PIXEL_RIGHT, self.switch_b_toggled)
        self.power_switch = GameThreeWaySwitch(self.pixels, POWER_SWITCH_A_PIN, POWER_SWITCH_B_PIN, POWER_SWITCH_TOP_PIXELS, POWER_SWITCH_BOTTOM_PIXELS, self.power_switch_toggled)
        self.elevator_buttons = GameElevatorButtons(self.pixels, ELEVATOR_BUTTONS_PINS, ELEVATOR_BUTTONS_PIXELS, self.elevator_button_pressed)

        # self.game = game.GhostAudioGameLogic(self.green_button, self.red_button, self.switch_a, self.switch_b, self.power_switch, self.switchboard, self.elevator_buttons, self.mqtt, self.sound, on_change_mode=self._on_change_mode)
        # self._update_deco_lights()
        self.mqtt.listen(self.__parse_mqtt_event)

    def _on_change_mode(self, mode):
        print("Mode changed to", mode)
        if mode in [game.GAME_MODE_OFF, game.GAME_MODE_WIN, game.GAME_MODE_LOSE]:
            self.current_rfid = None
        self._update_deco_lights()

    def _update_deco_lights(self):

        if self.game.mode in [game.GAME_MODE_SCANNING, game.GAME_MODE_READY]:
            self.headphone_routine = Routines.PulseRoutine(self.pixels, HEADPHONE_DECO_PIXELS_TOP + HEADPHONE_DECO_PIXELS_BOTTOM, Colors.green, 0.05)
        elif self.game.mode in [game.GAME_MODE_ROUND_START, game.GAME_MODE_RUNNING]:
            self.headphone_routine = Routines.ColorRoutine(self.pixels, HEADPHONE_DECO_PIXELS_TOP + HEADPHONE_DECO_PIXELS_BOTTOM, Colors.green)
        elif self.game.mode in [game.GAME_MODE_WIN, game.GAME_MODE_LOSE]:
            self.headphone_routine = Routines.PulseRoutine(self.pixels, HEADPHONE_DECO_PIXELS_TOP + HEADPHONE_DECO_PIXELS_BOTTOM, Colors.red, 0.5)
        else:
            self.headphone_routine = Routines.BlackoutRoutine(self.pixels, HEADPHONE_DECO_PIXELS_TOP + HEADPHONE_DECO_PIXELS_BOTTOM)

        if self.game.mode is game.GAME_MODE_OFF:
            self.deco_routine = Routines.MushroomRoutine(self.pixels, SWITCHBOARD_DECO_PIXELS + PEDESTAL_DECO_PIXELS)
        elif self.game.mode in [game.GAME_MODE_SCANNING, game.GAME_MODE_READY]:
            self.deco_routine = Routines.FireRoutine(self.pixels, SWITCHBOARD_DECO_PIXELS + PEDESTAL_DECO_PIXELS, [Colors.light_green])
        elif self.game.mode in [game.GAME_MODE_ROUND_START, game.GAME_MODE_RUNNING]:
            self.deco_routine = Routines.ColorRoutine(self.pixels, SWITCHBOARD_DECO_PIXELS + PEDESTAL_DECO_PIXELS, Colors.green)
        elif self.game.mode is game.GAME_MODE_WIN:
            self.deco_routine = Routines.RainbowRoutine(self.pixels, SWITCHBOARD_DECO_PIXELS + PEDESTAL_DECO_PIXELS)
        elif self.game.mode is game.GAME_MODE_LOSE:
            self.deco_routine = Routines.PulseRoutine(self.pixels, SWITCHBOARD_DECO_PIXELS + PEDESTAL_DECO_PIXELS, Colors.red, 0.5)

    def green_button_pressed(self):
        print("Green Button pressed")
        self.update()

    def red_button_pressed(self):
        print("Red Button pressed")
        self.update()

    def switch_a_toggled(self, value):
        completed = self.switch_a.desired_mode == value
        print("Switch A toggled", value, completed)
        self.update()

    def switch_b_toggled(self, value):
        completed = self.switch_b.desired_mode == value
        print("Switch B toggled", value, completed)
        self.update()

    def power_switch_toggled(self, value):
        completed = self.power_switch.desired_mode == value
        print("Power Switch toggled", value, completed)
        self.update()

    def elevator_button_pressed(self, button_num):
        print("Elevator Button pressed")
        self.update()

    def __parse_mqtt_event(self, event):
        try:
            events = json.loads(event)
            if not type(events) in (tuple, list):
                events = [events]
            for data in events:
                if data and data["event"]:
                    event = data["event"]
                    if event == EVENT_CARD_FOUND or event == EVENT_CARD_REMOVED or event == EVENT_FINISHED_BOOT:
                        reader_name = data["reader"]
                        if reader_name == self.id:
                            if event == EVENT_CARD_FOUND:
                                card_id = data["card"]
                                self.__on_card_detected(card_id)
                            elif event == EVENT_CARD_REMOVED:
                                self.__on_card_removed()
                            elif event == EVENT_FINISHED_BOOT:
                                pass
                                # Nothing yet
        except Exception as e:
            print("Artifact Failed parsing event", event, e)

    def __on_card_detected(self, card):
        print("Card detected", card)
        if self.current_rfid != card and self.game.mode not in [game.GAME_MODE_RUNNING, game.GAME_MODE_ROUND_START, game.GAME_MODE_WIN]:
            self.current_rfid = card
            self.game.start_scanning(self.current_rfid)

    def __on_card_removed(self):
        print("card removed")
        # self.current_rfid = None
        # self.next_event_time = 0

    def update(self):
        # try:
        # self.game.update()
        self.green_button.tick()
        self.red_button.tick()
        self.switch_a.tick()
        self.switch_b.tick()
        self.power_switch.tick()
        self.elevator_buttons.tick()
        self.switchboard.update()
        self.deco_routine.tick()
        self.headphone_routine.tick()
        self.pixels.render()
        self.mqtt.publish_batch()
        # except Exception as e:
        #     print("Audio Machine failed to update", e)
