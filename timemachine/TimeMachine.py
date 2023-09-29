from timemachine.Levers import *
import arrow
import math


END = arrow.get('2999-12-31 23:59:59', 'YYYY-MM-DD HH:mm:ss')
START = arrow.get('1000-1-1 00:00:00', 'YYYY-MM-DD HH:mm:ss')
# 10 years every second at full speed
SPEED_MULTIPLIER = -100/1000 * 60 * 60 * 24 * 365
ZERO_TOLERANCE = 0.1
MIN_UPDATE_TIME = 0.250


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
        log_value = math.log10(abs(speed * 10))
        if is_negative:
            log_value = log_value * -1
        return log_value

    def update(self):
        self.levers.update()
        if self.active:
            now = arrow.now()
            time_delta = now - self.last_event
            if time_delta > MIN_UPDATE_TIME:
                change = self.speed * SPEED_MULTIPLIER * time_delta
                date_ts = self.date.float_timestamp
                new_date_ts = round(date_ts + change)
                new_date = arrow.get(new_date_ts)
                if new_date > END:
                    new_date = END
                if new_date < START:
                    new_date = START
                if new_date != self.date:
                    print(f"Date changed to {print_datetime(new_date)}")
                    self.date = new_date


