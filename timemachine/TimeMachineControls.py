import RPi.GPIO as GPIO
import math
from datetime import datetime, timedelta
import time
import json
import random

from lighting.routines import Routines
from timemachine.Levers import *
from mqtt.MqttClient import *
from timemachine.CoinMachine import CoinMachine
from lighting.PixelControl import PixelControl
from timemachine.Button import Button
from timemachine.ThreeWaySwitch import ThreeWaySwitch
from timemachine.TimeMachineSoundSystem import TimeMachineSoundSystem, STARTUP_TIME


ZERO = datetime.fromtimestamp(0)
END = datetime(2999, 12, 31, 23, 59, 59)
START = datetime(1000, 1, 1, 0, 0, 0)
# 10 years every second at full speed
SPEED_MULTIPLIER = -(60 * 60 * 24 * 365) * 10
ZERO_TOLERANCE = 0.1
MIN_UPDATE_TIME = 0
RUN_DURATION_S = 240

NUM_LEDS = 50
PIXEL_SPEED_START = 0
PIXEL_SPEED_END = 8
PIXEL_POWER_START = 29
PIXEL_POWER_END = 37
PIXEL_MODE_START = 11
PIXEL_MODE_END = 18
PIXEL_SWITCH_START = 23
PIXEL_SWITCH_END = 25
PIXELS_SPEED = range(PIXEL_SPEED_START, PIXEL_SPEED_END + 1)
PIXELS_POWER = range(PIXEL_POWER_START, PIXEL_POWER_END + 1)
PIXELS_MODE = (11, 12, 13, 14, 15, 16, 18, 19)  # range(PIXEL_MODE_START, PIXEL_MODE_END + 1)
PIXELS_SWITCH = list(reversed(range(PIXEL_SWITCH_START, PIXEL_SWITCH_END + 1)))

MODE_TOGGLE_UP = 16
MODE_TOGGLE_DOWN = 13
ACTIVATE_BUTTON = 22
ACTIVATE_BUTTON_LIGHT = 23
MODE_BUTTON = 25
MODE_BUTTON_LIGHT = 24
COUNTDOWN_BUTTON = 28  # ???
COUNTDOWN_BUTTON_LIGHT = 29  # ???

COUNTDOWN_LENGTH = 11


def print_datetime(date):
    return date.strftime('%Y/%m/%d  %H:%M:%S')


class TimeMachineControls(object):
    levers = None
    mqtt = MqttClient()
    coin = CoinMachine()
    music = TimeMachineSoundSystem()

    date = END
    speed = 0
    is_stopped = False
    active = False
    last_event = time.time()
    is_charged = False
    is_starting_up = False
    start_time = 0
    freq_mode = 1
    color_mode = 1
    magnitude = 0
    raw_lever_value = 0
    is_countdown = False
    countdown_start_time = 0

    pixels = PixelControl(NUM_LEDS, led_pin=21)
    power_routine = Routines.PowerGaugeRoutine(pixels, PIXELS_POWER)
    speed_routine = Routines.SpeedGaugeRoutine(pixels, PIXELS_SPEED)
    mode_routine = Routines.ModeRoutine(pixels, PIXELS_MODE)
    mode_switch_routine = Routines.ModeSwitchRoutine(pixels, PIXELS_SWITCH)
    light_routines = Routines.MultiRoutine([power_routine, speed_routine, mode_routine, mode_switch_routine])

    activate_button = None
    mode_button = None
    countdown_button = None

    def __init__(self):
        # GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        self.levers = Levers(self.__on_lever_change, self.__on_button_change)
        self.coin.start_waiting_for_coin(self.__on_coin_accepted)
        self.date = END
        self.speed = 0
        self.magnitude = 0
        self.__on_change_data()

        self.activate_button = Button(ACTIVATE_BUTTON, ACTIVATE_BUTTON_LIGHT, self.__on_activate)
        self.activate_button.set_light(False)
        self.mode_button = Button(MODE_BUTTON, MODE_BUTTON_LIGHT, self.__on_mode_button)
        self.mode_button.set_light(True)
        self.mode_switch = ThreeWaySwitch(MODE_TOGGLE_UP, MODE_TOGGLE_DOWN, self.__on_mode_switch)

        # self.countdown_button = Button(COUNTDOWN_BUTTON, COUNTDOWN_BUTTON_LIGHT, self.__on_countdown_button)
        # self.countdown_button.set_light(True)

        self.mqtt.listen(self.__on_event)

    def __on_event(self, event):
        data = json.loads(event)
        if data and data["event"] == "countdownButton":
            self.__on_countdown_button()

    def __on_lever_change(self, lever_id, value):
        if self.is_starting_up:
            print("Startup lever change")
            value = 0.94
        if lever_id == 1 and self.raw_lever_value != value:
            # print(f"Got lever {id} change to {value}")
            modified_value = value * 100 * -1
            modified_prev_value = self.raw_lever_value * 100 * -1
            if abs(modified_value - modified_prev_value) > 1 and not self.is_countdown:
                rounded_value = round(modified_value)
                self.raw_lever_value = value
                self.magnitude = rounded_value * 10
                self.speed = self.__scale_speed(rounded_value / 100)
                print(f"magnitude: {self.magnitude} - speed: {self.speed}")
                if not self.active:
                    self.__on_change_data()

    def __on_mode_button(self):
        self.freq_mode = self.freq_mode + 1
        if self.freq_mode > 8:
            self.freq_mode = 1
        self.mode_routine.update_mode(self.freq_mode)
        print(f"Mode set to {self.freq_mode}")
        self.__on_change_data()

    def __on_mode_switch(self, mode):
        self.color_mode = mode
        self.mode_switch_routine.update_mode(mode)
        self.__on_change_data()

    def __on_countdown_button(self):
        if self.active:
            print("Starting Countdown")
            self.is_countdown = True
            self.magnitude = 150
            self.speed = self.__scale_speed(0.15)
            self.__on_change_data()

    def __on_button_change(self, id, value):
        print(f"Got button {id} change to {value}")

    def __on_activate(self):
        print("Activate Pressed")
        if self.is_charged:
            self.__start_machine()

    def __on_coin_accepted(self):
        print("Time Machine has a coin!")
        self.is_charged = True
        self.activate_button.flash_light(0.2)
        if self.active:
            self.power_routine.update_percentage(1)
            now = time.time()
            self.last_event = now
            self.start_time = now
            self.coin.clear_coins()
            self.is_charged = False
            self.is_starting_up = False
            self.activate_button.set_light(False)

    def __start_machine(self):
        if self.is_charged:
            print("Starting Machine")
            self.activate_button.set_light(False)
            self.active = False
            self.is_starting_up = True
            self.__on_lever_change(1, 0.8)
            self.power_routine.update_percentage(1)
            now = time.time()
            self.start_time = now
            self.coin.clear_coins()
            self.__on_change_data()

    def __scale_speed(self, speed):
        is_negative = speed < 0
        value = 10 ** (abs(speed) * 12.4)
        if is_negative and value is not 0:
            value = value * -1
        return value

    def __on_change_data(self):

        data = {
            "active": self.active,
            "startup": self.is_starting_up,
            "event": "timechange",
            "date": print_datetime(self.date),
            "timestamp": (self.date - START).total_seconds(),
            "speed": self.speed,
            "freq_mode": self.freq_mode,
            "color_mode": self.color_mode,
            "magnitude": self.magnitude
        }
        self.mqtt.publish(json.dumps(data))

    def update(self):
        self.levers.update()
        now = time.time()
        if self.is_starting_up:
            if now > self.start_time + STARTUP_TIME:
                print("Startup Done")
                self.active = True
                self.start_time = now
                self.is_starting_up = False
                self.__on_lever_change(1, self.raw_lever_value)

        if self.active or self.is_starting_up:
            percent_power = 1 - ((now - self.start_time) / RUN_DURATION_S)
            self.power_routine.update_percentage(percent_power)

            if now > self.countdown_start_time + COUNTDOWN_LENGTH:
                self.is_countdown = False

            if percent_power <= 0:
                print("Machine has ran out of power!  Shutting down...")
                self.is_charged = False
                self.active = False
                self.is_countdown = False
                self.speed = 0
                self.date = END
                self.__on_change_data()
                self.speed_routine.update_magnitude(0)
                self.speed_routine.update_active(False)
                self.speed_routine.tick()
                self.power_routine.update_percentage(0)
            else:
                time_delta = now - self.last_event
                if time_delta > MIN_UPDATE_TIME:
                    change = round(self.speed * time_delta)
                    delta = timedelta(milliseconds=change)
                    try:
                        new_date = self.date + delta
                    except OverflowError:
                        new_date = self.date
                        print(f"Date Overflow: {self.date} + {delta}")
                    if new_date > END:
                        new_date = END  # Temporary hack for testing
                        change = 0
                        self.magnitude = 0
                        self.speed = 0
                    if new_date < START:
                        new_date = START  # Temporary hack for testing
                        change = 0
                        self.magnitude = 0
                        self.speed = 0
                    # self.magnitude = self.magnitude if change != 0 else 0
                        # self.speed = change
                        # if change == 0:
                        #     self.magnitude = 0
                    self.is_stopped = change == 0
                    self.speed_routine.update_active(True)
                    self.speed_routine.update_magnitude(self.magnitude)

                        # print(f"Date changed to {print_datetime(new_date)} - speed {round(self.speed)}")
                    self.date = new_date
                    self.__on_change_data()
                    self.last_event = now
        self.music.update_sounds(self.active or self.is_starting_up, self.magnitude, self.is_countdown)
        self.light_routines.tick()
        self.pixels.render()
        self.activate_button.tick()


