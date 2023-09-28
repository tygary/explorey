from timemachine.Levers import *
import time
import math

MAX_YEAR = 2999
MIN_YEAR = 1900
# 10 years every second at full speed
SPEED_MULTIPLIER = -100/1000
ZERO_TOLERANCE = 0.1
MIN_UPDATE_TIME = 0.250


class TimeMachine(object):
    levers = None
    year = MAX_YEAR
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
        log_value = math.log10(abs(speed * 10))
        if is_negative:
            log_value = log_value * -1
        return log_value



    def update(self):
        self.levers.update()
        if self.active:
            now = time.time()
            time_delta = now - self.last_event
            if time_delta > MIN_UPDATE_TIME:
                change = self.speed * SPEED_MULTIPLIER * time_delta
                new_year = round(self.year + change)
                if new_year > MAX_YEAR:
                    new_year = MAX_YEAR
                if new_year < MIN_YEAR:
                    new_year = MIN_YEAR
                if new_year != self.year:
                    print(f"Year changed to {new_year}")
                    self.year = new_year


