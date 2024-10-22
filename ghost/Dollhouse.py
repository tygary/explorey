import json
import random
import time
import RPi.GPIO as GPIO

from lighting.PixelControl import PixelControl
from lighting.Colors import Colors
from lighting.routines import Routines
from mqtt.MqttClient import MqttClient

from timemachine.Button import Button


EVENT_CARD_FOUND = "cardFound"
EVENT_CARD_REMOVED = "cardRemoved"
EVENT_FINISHED_BOOT = "finishedBoot"
EVENT_GHOST_UPDATE = "ghostUpdate"
EVENT_RESET_COMMAND = "reset"
EVENT_OPEN_DOOR_COMMAND = "openDoor"
EVENT_WRITE_RFID_COMMAND = "writeRfid"

BUTTON_ONE = 0
BUTTON_TWO = 1
BUTTON_THREE = 2
BUTTON_FOUR = 3
BUTTON_FIVE = 4

BUTTON_ONE_PIXELS = range(0, 10)
BUTTON_TWO_PIXELS = range(11, 20)
BUTTON_THREE_PIXELS = range(21, 30)
BUTTON_FOUR_PIXELS = range(31, 40)
BUTTON_FIVE_PIXELS = range(41, 50)
BUTTON_PIXEL_ADDRESSES = [BUTTON_ONE_PIXELS, BUTTON_TWO_PIXELS, BUTTON_THREE_PIXELS, BUTTON_FOUR_PIXELS, BUTTON_FIVE_PIXELS]

BUTTON_PINS = [1, 2, 3, 4, 5]

MODE_GAME_PLAYING = 0
MODE_GAME_WON = 1

WIN_TIME_LENGTH_S = 20


WINNING_ORDER = [BUTTON_THREE, BUTTON_FOUR, BUTTON_FIVE, BUTTON_ONE, BUTTON_TWO]

MATRIX_CHANGES = [
    [1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 1, 1, 0]
]


class Dollhouse(object):
    id = "dollhouse"
    mqtt = None
    pixels = None
    current_rfid = None
    buttons = []
    light_routines = []

    reset_time = None

    mode = MODE_GAME_PLAYING
    state = [False, False, False, False, False]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pixels = PixelControl(700, led_brightness=180, led_pin=21)
        self.mqtt = MqttClient()

        def get_callback(button_num):
            def button_num_callback():
                return self.button_pressed(button_num)
            return button_num_callback
        self.buttons = [
            # Button(BUTTON_PINS[BUTTON_ONE], callback=get_callback(BUTTON_ONE)),
            # Button(BUTTON_PINS[BUTTON_TWO], callback=get_callback(BUTTON_TWO)),
            # Button(BUTTON_PINS[BUTTON_THREE], callback=get_callback(BUTTON_THREE)),
            # Button(BUTTON_PINS[BUTTON_FOUR], callback=get_callback(BUTTON_FOUR)),
            # Button(BUTTON_PINS[BUTTON_FIVE], callback=get_callback(BUTTON_FIVE)),
        ]

        self.light_routines = Routines.MultiRoutine([
            Routines.ColorRoutine(self.pixels, BUTTON_ONE_PIXELS, color=Colors.bright_white),
            Routines.ColorRoutine(self.pixels, BUTTON_TWO_PIXELS, color=Colors.bright_white),
            Routines.ColorRoutine(self.pixels, BUTTON_THREE_PIXELS, color=Colors.bright_white),
            Routines.ColorRoutine(self.pixels, BUTTON_FOUR_PIXELS, color=Colors.bright_white),
            Routines.ColorRoutine(self.pixels, BUTTON_FIVE_PIXELS, color=Colors.bright_white)
        ])

        self.mqtt.listen(self.__parse_mqtt_event)
        self.reset()

    def button_pressed(self, button_num):
        print(f"Button {button_num} pressed")
        old_state = self.state
        matrix = MATRIX_CHANGES[button_num]
        self.state = [
            old_state[i] and matrix[i] for i in range(0, 5)
        ]
        self.state[button_num] = 1
        has_turned_off = False
        all_lights_on = True
        for i in range(0, 5):
            if not self.state[i]:
                all_lights_on = False
            if old_state[i] and not self.state[i]:
                has_turned_off = True
                print(f"Turned off index {i}")
                self.turn_off_light(i)
            elif not old_state[i] and self.state[i]:
                print(f"Turned on index {i}")
                self.turn_on_light(i)
        if has_turned_off:
            print("Turned off some lights!")
            # Play sounds?
        if all_lights_on:
            self.win_game()

    def turn_on_light(self, index):
        self.light_routines.routines[index] = Routines.ColorRoutine(self.pixels, BUTTON_PIXEL_ADDRESSES[index], color=Colors.soft_white)

    def turn_off_light(self, index):
        self.light_routines.routines[index] = Routines.BlackoutRoutine(self.pixels, BUTTON_PIXEL_ADDRESSES[index])

    def win_game(self):
        self.mqtt.queue_in_batch_publish({
            "event": EVENT_GHOST_UPDATE,
            "reader": self.id,
            "id": self.id,
            "command": EVENT_OPEN_DOOR_COMMAND
        })
        self.reset_time = time.time() + WIN_TIME_LENGTH_S

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

    def __on_card_removed(self):
        print("card removed")
        self.current_rfid = None

    def update(self):
        if self.reset_time and self.reset_time > time.time():
            self.reset()
        for button in self.buttons:
            button.tick()
        self.light_routines.tick()
        self.pixels.render()

    def reset(self):
        self.mode = MODE_GAME_PLAYING
        self.reset_time = None
        self.state = [False, False, False, False, False]
        # self.turn_off_light(0)
        # self.turn_off_light(1)
        # self.turn_off_light(2)
        # self.turn_off_light(3)
        # self.turn_off_light(4)
        self.mqtt.queue_in_batch_publish({
            "event": EVENT_GHOST_UPDATE,
            "reader": self.id,
            "id": self.id,
            "command": EVENT_RESET_COMMAND
        })





