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
PIXEL_POWER_START = 13
PIXEL_POWER_END = 22
PIXELS_SPEED = range(PIXEL_SPEED_START, PIXEL_SPEED_END + 1)
PIXELS_POWER = range(PIXEL_POWER_START, PIXEL_POWER_END + 1)


def print_datetime(date):
    return date.strftime('%Y/%m/%d  %H:%M:%S')


class TimeMachine(object):
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

    pixels = PixelControl(NUM_LEDS)
    power_routine = PowerGaugeRoutine(pixels, PIXELS_POWER)
    speed_routine = SpeedGaugeRoutine(pixels, PIXELS_SPEED)
    light_routines = MultiRoutine([power_routine, speed_routine])

    def __init__(self):
        # GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        self.levers = Levers(self.__on_lever_change, self.__on_button_change)
        self.coin.start_waiting_for_coin(self.__on_coin_accepted)
        self.__on_change_date(END, 0)

    def __on_lever_change(self, id, value):
        # print(f"Got lever {id} change to {value}")
        self.magnitude = round(value * 1000) * -1
        self.speed = self.__scale_speed(value)

    def __on_button_change(self, id, value):
        print(f"Got button {id} change to {value}")

    def __on_coin_accepted(self):
        print("Time Machine has a coin!")
        self.is_charged = True
        self.__start_machine()

    def __start_machine(self):
        if self.is_charged:
            self.active = True
            self.start_time = time.time()
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
            "speed": speed,
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
                    new_date = START
                    change = 0
                if new_date < START:
                    new_date = END
                    change = 0
                if new_date != self.date or (change == 0 and not self.is_stopped):
                    self.is_stopped = change == 0
                    self.speed_routine.update_active(True)
                    self.speed_routine.update_magnitude(self.magnitude if change != 0 else 0)

                    print(f"Date changed to {print_datetime(new_date)} - speed {round(self.speed)}")
                    self.__on_change_date(new_date, change)
                self.last_event = now
        self.light_routines.tick()
        self.pixels.render()


