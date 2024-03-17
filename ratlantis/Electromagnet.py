import RPi.GPIO as GPIO
import time

ON = 0
OFF = 1


class Electromagnet(object):
    pin = None
    isOff = False
    turn_on_at = None

    def __init__(self, pin):
        self.pin = pin
        if pin > 0:
            GPIO.setup(pin, GPIO.OUT)

    def __set_value(self, value):
        GPIO.output(self.pin, value)

    def turn_off(self, time_s=2):
        print("Disabling Magnet")
        self.__set_value(OFF)
        self.turn_on_at = time.time() + time_s

    def update(self):
        if self.turn_on_at and time.time() > self.turn_on_at:
            print("Enabling Magnet")
            self.__set_value(ON)
            self.turn_on_at = None
