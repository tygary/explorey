from timemachine.Levers import *
from mqtt.MqttClient import *
import math
from datetime import datetime, timedelta
import time
import json


ZERO = datetime.fromtimestamp(0)
END = datetime(2999, 12, 31, 23, 59, 59)
START = datetime(1000, 1, 1, 0, 0, 0)
# 10 years every second at full speed
SPEED_MULTIPLIER = -(60 * 60 * 24 * 365) * 10
ZERO_TOLERANCE = 0.1
MIN_UPDATE_TIME = 0


def print_datetime(date):
    return date.strftime('%Y/%m/%d  %H:%M:%S')


class TimeMachine(object):
    levers = None
    date = END
    speed = 0
    is_stopped = False
    active = True
    last_event = time.time()
    mqtt = MqttClient()

    def __init__(self):
        self.levers = Levers(self.__on_lever_change, self.__on_button_change)

    def __on_lever_change(self, id, value):
        # print(f"Got lever {id} change to {value}")
        self.magnitude = round(value * 1000)
        self.speed = self.__scale_speed(value)

    def __on_button_change(self, id, value):
        print(f"Got button {id} change to {value}")

    def __scale_speed(self, speed):
        # if abs(speed) < ZERO_TOLERANCE:
        #     print(f"Time has stopped!!!")
        #     return 0
        is_negative = speed > 0
        value = 10 ** (abs(speed) * 12.4)
        if is_negative and value is not 0:
            value = value * -1
        return value

    def __on_change_date(self, new_date, speed):
        self.date = new_date
        data = {
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
            time_delta = now - self.last_event
            if time_delta > MIN_UPDATE_TIME:
                change = round(self.speed * time_delta)
                delta = timedelta(milliseconds=change)
                new_date = self.date + delta
                if new_date > END:
                    new_date = END
                    change = 0
                if new_date < START:
                    new_date = START
                    change = 0
                if new_date != self.date or (change == 0 and not self.is_stopped):
                    self.is_stopped = change == 0
                    print(f"Date changed to {print_datetime(new_date)} - speed {round(self.speed)}")
                    self.__on_change_date(new_date, change)
                self.last_event = now


