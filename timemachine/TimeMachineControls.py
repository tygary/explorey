import RPi.GPIO as GPIO
import math
from datetime import datetime, timedelta
import time
import json

from timemachine.Levers import *
from mqtt.MqttClient import *
from timemachine.CoinMachine import CoinMachine
from lighting.PixelControl import PixelControl
from lighting.Routine import *
from timemachine.Button import Button
from timemachine.ThreeWaySwitch import ThreeWaySwitch


ZERO = datetime.fromtimestamp(0)
END = datetime(2999, 12, 31, 23, 59, 59)
START = datetime(1000, 1, 1, 0, 0, 0)
# 10 years every second at full speed
SPEED_MULTIPLIER = -(60 * 60 * 24 * 365) * 10
ZERO_TOLERANCE = 0.1
MIN_UPDATE_TIME = 0
RUN_DURATION_S = 60

NUM_LEDS = 50
PIXEL_SPEED_START = 0
PIXEL_SPEED_END = 8
PIXEL_POWER_START = 28
PIXEL_POWER_END = 36
PIXEL_MODE_START = 11
PIXEL_MODE_END = 18
PIXEL_SWITCH_START = 23
PIXEL_SWITCH_END = 25
PIXELS_SPEED = range(PIXEL_SPEED_START, PIXEL_SPEED_END + 1)
PIXELS_POWER = range(PIXEL_POWER_START, PIXEL_POWER_END + 1)
PIXELS_MODE = range(PIXEL_MODE_START, PIXEL_MODE_END + 1)
PIXELS_SWITCH = list(reversed(range(PIXEL_SWITCH_START, PIXEL_SWITCH_END + 1)))

MODE_TOGGLE_UP = 16
MODE_TOGGLE_DOWN = 13
ACTIVATE_BUTTON = 22
ACTIVATE_BUTTON_LIGHT = 23
MODE_BUTTON = 25
MODE_BUTTON_LIGHT = 24


def print_datetime(date):
    return date.strftime('%Y/%m/%d  %H:%M:%S')


class TimeMachineControls(object):
    levers = None
    mqtt = MqttClient()
    coin = CoinMachine()

    date = END
    speed = 0
    is_stopped = False
    active = False
    last_event = time.time()
    is_charged = False
    start_time = 0
    mode = 1
    color_mode = 1

    pixels = PixelControl(NUM_LEDS)
    power_routine = PowerGaugeRoutine(pixels, PIXELS_POWER)
    speed_routine = SpeedGaugeRoutine(pixels, PIXELS_SPEED)
    mode_routine = ModeRoutine(pixels, PIXELS_MODE)
    mode_switch_routine = ModeSwitchRoutine(pixels, PIXELS_SWITCH)
    light_routines = MultiRoutine([power_routine, speed_routine, mode_routine, mode_switch_routine])

    activate_button = None
    mode_button = None

    def __init__(self):
        # GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        self.levers = Levers(self.__on_lever_change, self.__on_button_change)
        self.coin.start_waiting_for_coin(self.__on_coin_accepted)
        self.__on_change_date(END, 0)

        self.activate_button = Button(ACTIVATE_BUTTON, ACTIVATE_BUTTON_LIGHT, self.__on_activate)
        self.mode_button = Button(MODE_BUTTON, MODE_BUTTON_LIGHT, self.__on_mode_button)
        self.mode_button.set_light(True)
        self.mode_switch = ThreeWaySwitch(MODE_TOGGLE_UP, MODE_TOGGLE_DOWN, self.__on_mode_switch)

    def __on_lever_change(self, id, value):
        # print(f"Got lever {id} change to {value}")
        self.magnitude = round(value * 1000) * -1
        self.speed = self.__scale_speed(value)

    def __on_mode_button(self):
        self.mode = self.mode + 1
        if self.mode > 8:
            self.mode = 1
        self.mode_routine.update_mode(self.mode)
        print(f"Mode set to {self.mode}")

    def __on_mode_switch(self, mode):
        self.color_mode = mode
        self.mode_switch_routine.update_mode(mode)


    def __on_button_change(self, id, value):
        print(f"Got button {id} change to {value}")

    def __on_activate(self):
        print("Activate Pressed")
        if not self.active and self.is_charged:
            self.__start_machine()
            self.activate_button.set_light(False)


    def __on_coin_accepted(self):
        print("Time Machine has a coin!")
        self.is_charged = True
        self.activate_button.flash_light()

    def __start_machine(self):
        if self.is_charged:
            print("Starting Machine")
            self.active = True
            now = time.time()
            self.last_event = now
            self.start_time = now
            self.coin.clear_coins()

    def __scale_speed(self, speed):
        is_negative = speed > 0
        value = 10 ** (abs(speed) * 12.4)
        if is_negative and value is not 0:
            value = value * -1
        return value

    def __on_change_date(self, new_date, speed):
        self.date = new_date
        data = {
            "active": self.active,
            "event": "timechange",
            "date": print_datetime(new_date),
            "timestamp": (new_date - START).total_seconds(),
            "speed": speed,
            "mode": self.mode,
            "magnitude": self.magnitude if speed != 0 else 0
        }
        self.mqtt.publish(json.dumps(data))

    def update(self):
        self.levers.update()
        if self.active:
            now = time.time()
            percent_power = 1 - ((now - self.start_time) / RUN_DURATION_S)
            self.power_routine.update_percentage(percent_power)

            if percent_power <= 0:
                print("Machine has ran out of power!  Shutting down...")
                self.is_charged = False
                self.active = False
                self.__on_change_date(END, 0)
                self.speed_routine.update_magnitude(0)
                self.speed_routine.update_active(False)
                self.power_routine.update_percentage(0)
                return

            time_delta = now - self.last_event
            if time_delta > MIN_UPDATE_TIME:
                change = round(self.speed * time_delta)
                delta = timedelta(milliseconds=change)
                new_date = self.date + delta
                if new_date > END:
                    new_date = START  # Temporary hack for testing
                    change = 0
                if new_date < START:
                    new_date = END  # Temporary hack for testing
                    change = 0
                if new_date != self.date or (change == 0 and not self.is_stopped):
                    self.is_stopped = change == 0
                    self.speed_routine.update_active(True)
                    self.speed_routine.update_magnitude(self.magnitude if change != 0 else 0)

                    # print(f"Date changed to {print_datetime(new_date)} - speed {round(self.speed)}")
                    self.__on_change_date(new_date, change)
                self.last_event = now
        self.light_routines.tick()
        self.pixels.render()
        self.activate_button.tick()


