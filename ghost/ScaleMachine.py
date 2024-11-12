import json
import time
import RPi.GPIO as GPIO
import math
import random

from lighting.PixelControl import OverlayedPixelControl, PixelControl
from lighting.Colors import Colors
from lighting.routines import Routines
from mqtt.MqttClient import MqttClient

from timemachine.Button import Button


EVENT_CARD_FOUND = "cardFound"
EVENT_CARD_REMOVED = "cardRemoved"
EVENT_FINISHED_BOOT = "finishedBoot"
EVENT_GHOST_UPDATE = "ghostUpdate"
EVENT_RESET_COMMAND = "reset"
EVENT_WRITE_NFC = "writeNfc"

EVENT_SET_RUNNING = "setRunning"
EVENT_SET_FINISHED = "setFinished"

BUTTON_ONE_PIN = 22
BUTTON_ONE_LIGHT_PIN = 23
BUTTON_TWO_PIN = 27
BUTTON_TWO_LIGHT_PIN = 18

MODE_OFF = 0
MODE_SCANNING = 1
MODE_READY_TO_PLAY = 2
MODE_PLAYING = 3
MODE_FINISHED = 4

TIME_BEFORE_RESETTING = 30
GAME_LENGTH_TIME = 60
RFID_SCAN_TIMEOUT = 3

POWER_BOARD = 0
POWER_BOARD_NUM_PIXELS = 40  # 250

POWER_BOARD_PIXELS = list(range(POWER_BOARD, POWER_BOARD + POWER_BOARD_NUM_PIXELS))

SCALE_ONE = "scaleOne"
SCALE_TWO = "scaleTwo"


class GhostScaleMachine(object):
    current_rfid_one = None
    rfid_one_timeout_time = 0
    ghost_one_power_level = 0
    current_rfid_two = None
    rfid_two_timeout_time = 0
    ghost_two_power_level = 0

    light_routines = []
    previous_middle = 0
    left_triggered_wave_routine = None
    right_triggered_wave_routine = None
    game_end_time = 0
    next_reset_time = 0
    previous_mode = MODE_OFF
    mode = MODE_OFF

    oscillated_balance = 50
    current_balance = 50
    last_game_balance_update = 0

    oscillation_period_ms = 1000
    oscillation_start_time_ms = 0
    oscillation_going_up = True
    oscillation_magnitude = 10

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.mqtt = MqttClient()
        self.buttonOne = Button(BUTTON_ONE_PIN, BUTTON_ONE_LIGHT_PIN, callback=self.button_one_pressed, pullup=True)
        self.buttonTwo = Button(BUTTON_TWO_PIN, BUTTON_TWO_LIGHT_PIN, callback=self.button_two_pressed, pullup=True)
        self.mqtt.listen(self.__parse_mqtt_event)
        self.pixels = OverlayedPixelControl(led_count=POWER_BOARD_NUM_PIXELS)
        self.reset()
        self._update_light_routines()

    def _update_light_routines(self):
        num_pixels = POWER_BOARD_NUM_PIXELS // 2

        if self.mode is MODE_OFF:
            self.light_routines = [
                # Routines.ColorRoutine(self.pixels, POWER_BOARD_PIXELS, [0, 50, 100], brightness=0.2),
                Routines.WaveRoutine(self.pixels, POWER_BOARD_PIXELS, [Colors.blue, Colors.mixed_blue, Colors.purple], wave_wait_time=10, pixel_wait_time=0, should_override=True, brightness=0.8, can_reverse=False),
                Routines.MushroomRoutine(self.pixels, POWER_BOARD_PIXELS, brightness=1.0),
                # Routines.RainbowRoutine(self.pixels, POWER_BOARD_PIXELS),
            ]
            self.left_triggered_wave_routine = None
            self.right_triggered_wave_routine = None

            # self.light_routines = [
            #     Routines.BlackoutRoutine(self.pixels, POWER_BOARD_PIXELS),
            # ]
        elif self.mode is MODE_SCANNING or self.mode is MODE_READY_TO_PLAY:
            middle = round(num_pixels / 2)
            left = POWER_BOARD_PIXELS[0:middle]
            right = POWER_BOARD_PIXELS[middle:]
            right.reverse()

            left_power_index = round((self.ghost_one_power_level / 6) * len(left)) if self.current_rfid_one else 0
            powered_left = left[:left_power_index]
            unpowered_left = left[left_power_index:]

            right_power_index = round((self.ghost_two_power_level / 6) * len(right)) if self.current_rfid_two else 0
            powered_right = right[:right_power_index]
            unpowered_right = right[right_power_index:]

            self.light_routines = [
                Routines.FireRoutine(self.pixels, powered_left, [Colors.light_green]),
                Routines.BlackoutRoutine(self.pixels, unpowered_left),
                Routines.FireRoutine(self.pixels, powered_right, [Colors.soft_blue]),
                Routines.BlackoutRoutine(self.pixels, unpowered_right),
            ]
            self.left_triggered_wave_routine = None
            self.right_triggered_wave_routine = None
        elif self.mode is MODE_PLAYING:
            middle = round((self.oscillated_balance / 100) * num_pixels)
            if middle != self.previous_middle:
                print("middle is ", middle)
                self.previous_middle = middle
                left = POWER_BOARD_PIXELS[0:middle]
                right = POWER_BOARD_PIXELS[middle:]
                right.reverse()

                if self.mode is not self.previous_mode:
                    self.light_routines = [
                        Routines.ColorRoutine(self.pixels, left, Colors.green, brightness=0.3),
                        Routines.ColorRoutine(self.pixels, right, Colors.red, brightness=0.3),
                    ]
                    self.left_triggered_wave_routine = Routines.TriggeredWaveRoutine(self.pixels, left, should_override=True, brightness=0.3)
                    self.right_triggered_wave_routine = Routines.TriggeredWaveRoutine(self.pixels, right, should_override=True, brightness=0.3)
                else:
                    self.light_routines[0].update_addresses(left)
                    self.light_routines[1].update_addresses(right)
                    self.left_triggered_wave_routine.update_addresses(left)
                    self.right_triggered_wave_routine.update_addresses(right)
        elif self.mode is MODE_FINISHED:
            self.left_triggered_wave_routine = None
            self.right_triggered_wave_routine = None
            middle = round(num_pixels / 2)
            left = POWER_BOARD_PIXELS[0:middle]
            right = POWER_BOARD_PIXELS[middle:]
            if self.current_balance > 50:
                self.light_routines = [
                    Routines.RainbowRoutine(self.pixels, left),
                    Routines.BlackoutRoutine(self.pixels, right),
                ]
            else:
                self.light_routines = [
                    Routines.BlackoutRoutine(self.pixels, left),
                    Routines.RainbowRoutine(self.pixels, right),
                ]
        self.previous_mode = self.mode

    def button_one_pressed(self):
        print("Button one pressed")
        if self.mode is MODE_READY_TO_PLAY:
            self.start_playing()
        elif self.mode is MODE_PLAYING:
            self.current_balance += 1
            print("Updated Balance", self.current_balance)
            self._update_light_routines()
            self.left_triggered_wave_routine.trigger(Colors.green, 2.0)
            # Play sound

    def button_two_pressed(self):
        print("Button two pressed")
        if self.mode is MODE_READY_TO_PLAY:
            self.start_playing()
        elif self.mode is MODE_PLAYING:
            self.current_balance -= 1
            print("Updated Balance", self.current_balance)
            self._update_light_routines()
            self.right_triggered_wave_routine.trigger(Colors.red, 2.0)
            # play sound

    def __parse_mqtt_event(self, event):
        # try:
        events = json.loads(event)
        if not type(events) in (tuple, list):
            events = [events]
        for data in events:
            if data and data["event"]:
                event = data["event"]
                if event == EVENT_CARD_FOUND or event == EVENT_CARD_REMOVED or event == EVENT_FINISHED_BOOT or event == EVENT_WRITE_NFC:
                    reader_name = data["reader"]
                    if reader_name in [SCALE_ONE, SCALE_TWO]:
                        print("Got MQTT Event", event)
                        if event == EVENT_CARD_FOUND:
                            card_id = data["card"]
                            power_level = data["power"]
                            self.__on_card_detected(card_id, reader_name, power_level)
                        elif event == EVENT_CARD_REMOVED:
                            self.__on_card_removed(reader_name)
                        elif event == EVENT_FINISHED_BOOT:
                            self.reset()
                        elif event == EVENT_WRITE_NFC:
                            card_id = data["card"]
                            power_level = data["power"]
                            self.__on_card_detected(card_id, reader_name, power_level)
                            # Nothing yet
        # except Exception as e:
        #     print("Artifact Failed parsing event", event, e)

    def __on_card_detected(self, card, reader_name, power_level):
        print("Card detected", card, reader_name, power_level)
        if reader_name == SCALE_ONE:
            current_rfid = self.current_rfid_one
            self.current_rfid_one = card
            self.ghost_one_power_level = power_level
            self.rfid_one_timeout_time = 0
        elif reader_name == SCALE_TWO:
            current_rfid = self.current_rfid_two
            self.current_rfid_two = card
            self.ghost_two_power_level = power_level
            self.rfid_two_timeout_time = 0
        if current_rfid != card:
            if self.mode not in [MODE_PLAYING, MODE_FINISHED]:
                if self.current_rfid_one and self.current_rfid_two:
                    self.start_ready_to_play()
                else:
                    self.start_scanning()
        self._update_light_routines()

    def __on_card_removed(self, reader_name):
        print("card removed")
        if self.mode in [MODE_SCANNING, MODE_READY_TO_PLAY]:
            if reader_name == SCALE_ONE:
                self.rfid_one_timeout_time = time.time() + RFID_SCAN_TIMEOUT
            elif reader_name == SCALE_TWO:
                self.rfid_two_timeout_time = time.time() + RFID_SCAN_TIMEOUT
        if self.mode in [MODE_FINISHED]:
            if reader_name == SCALE_ONE:
                self.current_rfid_one = None
            elif reader_name == SCALE_TWO:
                self.current_rfid_two = None
        if self.mode is MODE_SCANNING and not self.current_rfid_one and not self.current_rfid_two:
            self.mode = MODE_OFF
        self._update_light_routines()
            
        # self.current_rfid = None
        # self.mode = MODE_OFF
        # self.next_event_time = 0
        # self.button.set_light(False)

    def reset(self):
        self.mode = MODE_OFF
        self.rfid_one_timeout_time = 0
        self.rfid_two_timeout_time = 0
        self.next_reset_time = 0
        self.current_rfid_one = None
        self.ghost_one_power_level = 0
        self.current_rfid_two = None
        self.ghost_two_power_level = 0
        self.buttonOne.set_light(False)
        self.buttonTwo.set_light(False)
        self._update_light_routines()
        self.mqtt.queue_in_batch_publish({
            "event": EVENT_GHOST_UPDATE,
            "reader": SCALE_ONE,
            "id": SCALE_ONE,
            "command": EVENT_RESET_COMMAND,
        })
        self.mqtt.queue_in_batch_publish({
            "event": EVENT_GHOST_UPDATE,
            "reader": SCALE_TWO,
            "id": SCALE_TWO,
            "command": EVENT_RESET_COMMAND,
        })

    def start_scanning(self):
        print("Scanning trash")
        if self.mode is not MODE_SCANNING:
            self.mode = MODE_SCANNING
            self.buttonOne.set_light(False)
            self.buttonTwo.set_light(False)
            # Play sounds to start scanning
            self._update_light_routines()

    def start_ready_to_play(self):
        print("Ready to play")
        if self.mode is not MODE_READY_TO_PLAY:
            self.mode = MODE_READY_TO_PLAY
            self.next_reset_time = 0
            # self.next_reset_time = time.time() + TIME_BEFORE_RESETTING
            # Play sounds to start playing
            self.buttonOne.flash_light()
            self.buttonTwo.flash_light()

    def start_playing(self):
        print("Start Playing")
        self.mode = MODE_PLAYING
        self.previous_middle = 0
        self.rfid_one_timeout_time = 0
        self.rfid_two_timeout_time = 0
        self._update_light_routines()
        self.game_end_time = time.time() + GAME_LENGTH_TIME
        self.current_balance = 50
        self.last_game_balance_update = time.time()
        self.buttonOne.flash_light()
        self.buttonTwo.flash_light()
        self.mqtt.queue_in_batch_publish({
            "event": EVENT_GHOST_UPDATE,
            "reader": SCALE_ONE,
            "id": SCALE_ONE,
            "command": EVENT_SET_RUNNING,
        })
        self.mqtt.queue_in_batch_publish({
            "event": EVENT_GHOST_UPDATE,
            "reader": SCALE_TWO,
            "id": SCALE_TWO,
            "command": EVENT_SET_RUNNING,
        })

    def update_oscillation(self):
        if self.mode is not MODE_PLAYING:
            self.oscillated_balance = self.current_balance
            self.oscillation_start_time_ms = 0
            return
        now = time.time()
        now_ms = now * 1000

        if self.oscillation_start_time_ms < now_ms:
            self.oscillation_start_time_ms = now_ms + self.oscillation_period_ms
            self.oscillation_going_up = not self.oscillation_going_up
            percent_of_game = 1 - (self.game_end_time - now / GAME_LENGTH_TIME)
            print("oscillation flipping", self.oscillation_going_up)
            print("now", now)
            print("game end time", self.game_end_time)
            print("percent of game", percent_of_game)
            self.oscillation_magnitude = random.randrange(5, round(percent_of_game * 20 + 5))
            self.oscillation_period_ms = random.randrange(500, 2000)
            print("oscillation magnitude", self.oscillation_magnitude)
            print("oscillation period", self.oscillation_period_ms)
            
        if self.oscillation_going_up:
            self.oscillated_balance = self.current_balance + round(math.sin(math.pi * (now_ms - self.oscillation_start_time_ms) / self.oscillation_period_ms) * self.oscillation_magnitude)
        else:
            self.oscillated_balance = self.current_balance - round(math.sin(math.pi * (now_ms - self.oscillation_start_time_ms) / self.oscillation_period_ms) * self.oscillation_magnitude)
        print("oscillated balance", self.oscillated_balance)

    def start_end_game(self):
        print("Game Over")
        print("End Balance", self.current_balance)
        if self.current_balance > 50:
            print("Ghost One Wins")
        else:
            print("Ghost Two Wins")
        self.mode = MODE_FINISHED
        self.rfid_one_timeout_time = 0
        self.rfid_two_timeout_time = 0
        self.next_reset_time = time.time() + TIME_BEFORE_RESETTING
        self._update_light_routines()
        self.mqtt.queue_in_batch_publish({
            "event": EVENT_GHOST_UPDATE,
            "reader": SCALE_ONE,
            "id": SCALE_ONE,
            "command": EVENT_SET_FINISHED,
        })
        self.mqtt.queue_in_batch_publish({
            "event": EVENT_GHOST_UPDATE,
            "reader": SCALE_TWO,
            "id": SCALE_TWO,
            "command": EVENT_SET_FINISHED,
        })

    def update_game_balance(self):
        time_since_last_update = time.time() - self.last_game_balance_update
        if time_since_last_update > 1:
            self.last_game_balance_update = time.time()
            self.current_balance += self.ghost_one_power_level * 5 + self.ghost_two_power_level * -5
            # print("Updated Balance", self.current_balance)

    def update(self):
        if self.next_reset_time > 0 and self.next_reset_time < time.time():
            print("Timed out, resetting")
            self.reset()
        if self.rfid_one_timeout_time > 0 and self.rfid_one_timeout_time < time.time():
            print("Resetting rfid one")
            self.rfid_one_timeout_time = 0
            self.current_rfid_one = None
            self.ghost_one_power_level = 0
            if self.mode in [MODE_READY_TO_PLAY]:
                self.start_scanning()
            self._update_light_routines()
        if self.rfid_two_timeout_time > 0 and self.rfid_two_timeout_time < time.time():
            print("Resetting rfid two")
            self.current_rfid_two = None
            self.rfid_two_timeout_time = 0
            self.ghost_two_power_level = 0
            self._update_light_routines()
            if self.mode in [MODE_READY_TO_PLAY]:
                self.start_scanning()
            self._update_light_routines()
        if self.mode in [MODE_SCANNING, MODE_READY_TO_PLAY] and not self.current_rfid_one and not self.current_rfid_two:
            self.mode = MODE_OFF
            self.reset()
        if self.mode in [MODE_PLAYING]:
            self.update_game_balance()
            self.update_oscillation()
            if (self.game_end_time > 0 and self.game_end_time < time.time()) or self.current_balance <= 0 or self.current_balance >= 100:
                self.start_end_game()
            else:
                self._update_light_routines()

        for routine in self.light_routines:
            routine.tick()
        if self.left_triggered_wave_routine:
            self.left_triggered_wave_routine.tick()
        if self.right_triggered_wave_routine:
            self.right_triggered_wave_routine.tick()
        self.buttonOne.tick()
        self.buttonTwo.tick()
        self.pixels.render()
        self.mqtt.publish_batch()
