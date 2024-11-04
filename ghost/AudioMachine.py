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
EVENT_OPEN_DOOR_COMMAND = "openDoor"
EVENT_WRITE_RFID_COMMAND = "writeRfid"

BUTTON_PIN = 1

MODE_OFF = 0
MODE_SCANNING = 1
MODE_READY_TO_PRINT = 2

TIME_BEFORE_READY_TO_PRINT = 5

SWITCHBOARD_PINS = [24, 25, 13, 16]
RED_BUTTON_PIN = 17
GREEN_BUTTON_PIN = 4
SWITCH_A_PIN = 19
SWITCH_B_PIN = 20
POWER_SWITCH_A_PIN = 5
POWER_SWITCH_B_PIN = 6
ELEVATOR_BUTTONS_PINS = [7, 8, 9, 10]

SWITCHBOARD_PIXELS = [4, 3, 2, 1, 8, 9, 10, 11]
RED_BUTTON_PIXELS = [32, 33, 34, 35]
GREEN_BUTTON_PIXELS = [36, 37, 38, 39]
SWITCH_A_PIXEL_LEFT = 59
SWITCH_A_PIXEL_RIGHT = 60
SWITCH_B_PIXEL_LEFT = 61
SWITCH_B_PIXEL_RIGHT = 62
POWER_SWITCH_TOP_PIXELS = [30, 31]
POWER_SWITCH_BOTTOM_PIXELS = [26, 27]
ELEVATOR_BUTTONS_PIXELS = [46, 47, 48, 49, 50, 51, 52, 53]


class AudioMachine(object):
    id = "printer"
    current_rfid = None
    light_routines = []
    next_event_time = 0
    mode = MODE_OFF

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pixels = PixelControl(700, led_brightness=180, led_pin=21)
        self.mqtt = MqttClient()
        self.sound = GhostAudioSoundSystem()

        self.switchboard = Switchboard(self.pixels, [4, 3, 2, 1, 8, 9, 10, 11])
        self.green_button = GameButtonWithFourLights(self.pixels, GREEN_BUTTON_PIN, GREEN_BUTTON_PIXELS, self.green_button_pressed)
        self.red_button = GameButtonWithFourLights(self.pixels, RED_BUTTON_PIN, RED_BUTTON_PIXELS, self.red_button_pressed)
        self.switch_a = GameTwoWaySwitch(self.pixels, SWITCH_A_PIN, SWITCH_A_PIXEL_LEFT, SWITCH_A_PIXEL_RIGHT, self.switch_a_toggled)
        self.switch_b = GameTwoWaySwitch(self.pixels, SWITCH_B_PIN, SWITCH_B_PIXEL_LEFT, SWITCH_B_PIXEL_RIGHT, self.switch_b_toggled)
        self.power_switch = GameThreeWaySwitch(self.pixels, POWER_SWITCH_A_PIN, POWER_SWITCH_B_PIN, POWER_SWITCH_TOP_PIXELS, POWER_SWITCH_BOTTOM_PIXELS, self.power_switch_toggled)
        self.elevator_buttons = GameElevatorButtons(self.pixels, ELEVATOR_BUTTONS_PINS, ELEVATOR_BUTTONS_PIXELS, self.elevator_button_pressed)

        self.game = game.GhostAudioGameLogic(self.green_button, self.red_button, self.switch_a, self.switch_b, self.power_switch, self.switchboard, self.elevator_buttons, self.mqtt, self.sound)

        self.mqtt.listen(self.__parse_mqtt_event)

    def green_button_pressed(self):
        print("Green Button pressed")

    def red_button_pressed(self):
        print("Red Button pressed")

    def switch_a_toggled(self, value):
        completed = self.switch_a.desired_mode == value
        print("Switch A toggled", value, completed)

    def switch_b_toggled(self, value):
        completed = self.switch_b.desired_mode == value
        print("Switch B toggled", value, completed)

    def power_switch_toggled(self, value):
        completed = self.power_switch.desired_mode == value
        print("Power Switch toggled", value, completed)

    def elevator_button_pressed(self):
        print("Elevator Button pressed")

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
        self.current_rfid = card
        self.mode = MODE_SCANNING
        self.game._change_game_mode(game.GAME_MODE_SCANNING)
        self.next_event_time = time.time() + TIME_BEFORE_READY_TO_PRINT

    def __on_card_removed(self):
        print("card removed")
        self.current_rfid = None
        self.mode = MODE_OFF
        self.next_event_time = 0

    def update(self):
        # try:
        self.game.update()
        self.green_button.tick()
        self.red_button.tick()
        self.switch_a.tick()
        self.switch_b.tick()
        self.power_switch.tick()
        self.elevator_buttons.tick()
        self.switchboard.update()
        self.pixels.render()
        # except Exception as e:
        #     print("Audio Machine failed to update", e)
