from timemachine.Levers import *
import arrow
import math
from datetime import timedelta


END = arrow.get('2999-12-31 23:59:59', 'YYYY-MM-DD HH:mm:ss')
START = arrow.get('1000-01-01 00:00:00', 'YYYY-MM-DD HH:mm:ss')
# 10 years every second at full speed
SPEED_MULTIPLIER = -(60 * 60 * 24 * 365) * 10
ZERO_TOLERANCE = 0.1
MIN_UPDATE_TIME = timedelta(milliseconds=250)


def print_datetime(date):
    return date.ctime()


class TimeMachine(object):
    levers = None
    date = END
    speed = 0
    active = True
    last_event = arrow.now()

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
        log_value = math.log10(abs(speed * 1000)) / 3
        if is_negative:
            log_value = log_value * -1
        return log_value

    def update(self):
        self.levers.update()
        if self.active:
            now = arrow.now()
            time_delta = now - self.last_event
            if time_delta > MIN_UPDATE_TIME:
                print(f"time delta {time_delta.total_seconds()} - speed {self.speed} - multiplier {SPEED_MULTIPLIER}")
                change = self.speed * SPEED_MULTIPLIER * time_delta.total_seconds()
                date_ts = self.date.float_timestamp
                print(f"current date ts {date_ts} with change {change}")
                new_date_ts = date_ts + change
                print(f"new date ts = {new_date_ts}")
                new_date = arrow.get(new_date_ts)
                if new_date > END:
                    new_date = END
                if new_date < START:
                    new_date = START
                if new_date != self.date:
                    print(f"Date changed to {print_datetime(new_date)}")
                    self.date = new_date
                self.last_event = now


