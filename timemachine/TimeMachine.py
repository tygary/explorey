from timemachine.Levers import *
import math
from datetime import datetime, timedelta
import time


ZERO = datetime.fromtimestamp(0)
END = datetime(2999, 12, 31, 23, 59, 59)
START = datetime(1000, 1, 1, 0, 0, 0)
# 10 years every second at full speed
SPEED_MULTIPLIER = -(60 * 60 * 24 * 365) * 10
ZERO_TOLERANCE = 0.1
MIN_UPDATE_TIME = 0.250


def print_datetime(date):
    return date.strftime('%a, %d %b %Y %H:%M:%S')


class TimeMachine(object):
    levers = None
    date = END
    speed = 0
    active = True
    last_event = time.time()

    def __init__(self):
        self.levers = Levers(self.__on_lever_change, self.__on_button_change)

    def __on_lever_change(self, id, value):
        # print(f"Got lever {id} change to {value}")
        self.speed = self.__scale_speed(value)

    def __on_button_change(self, id, value):
        print(f"Got button {id} change to {value}")

    def __scale_speed(self, speed):
        # if abs(speed) < ZERO_TOLERANCE:
        #     print(f"Time has stopped!!!")
        #     return 0
        is_negative = speed < 0
        value = 10 ** (abs(speed) * 9)
        if is_negative and value is not 0:
            value = value * -1
        return value

    def update(self):
        self.levers.update()
        if self.active:
            now = time.time()
            time_delta = now - self.last_event
            if time_delta > MIN_UPDATE_TIME:
                change = round(self.speed * time_delta)
                delta = timedelta(seconds=change)
                new_date = self.date + delta
                if new_date > END:
                    new_date = END
                if new_date < START:
                    new_date = START
                if new_date != self.date:
                    print(f"Date changed to {print_datetime(new_date)} - speed {round(self.speed)}")
                    self.date = new_date
                self.last_event = now


