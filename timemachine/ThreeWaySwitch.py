import RPi.GPIO as GPIO
import time

from printer.addeventdetection import add_event_detection


class ThreeWaySwitch(object):
    pin_a = -1
    pin_b = -1
    callback = None

    def __init__(self, pin_a, pin_b, callback=None):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.callback = callback

        add_event_detection(self.pin_a, bothdirections=True, callback=self.__on_toggle, pullup=True)
        add_event_detection(self.pin_b, bothdirections=True, callback=self.__on_toggle, pullup=True)
        self.__on_toggle(-1)

    def __on_toggle(self, value):
        time.sleep(1)
        a = GPIO.input(self.pin_a)
        b = GPIO.input(self.pin_b)
        print(f"Switch toggled a:{a}, b:{b}")
        mode = 2
        if a is False:
            mode = 1
        elif b is False:
            mode = 3

        if self.callback:
            self.callback(mode)

