import RPi.GPIO as GPIO
import time

from printer.addeventdetection import add_event_detection


WAIT_TIME = 0.2
class Button(object):
    button_pin = -1
    button_light_pin = -1
    callback = None
    light_on = False
    is_flashing = False
    flash_length = 0.5
    next_flash = 0

    waiting = 0

    def __init__(self, button_pin, button_light_pin=-1, callback=None):
        self.button_pin = button_pin
        self.button_light_pin = button_light_pin
        self.callback = callback

        add_event_detection(self.button_pin, callback=self.__on_press)
        if button_light_pin > 0:
            GPIO.setup(self.button_light_pin, GPIO.OUT)


    def __on_press(self, value):
        now = time.time()
        if now > self.waiting:
            self.waiting = time.time() + WAIT_TIME
            if self.callback:
                self.callback()


    def set_light(self, on):
        GPIO.output(self.button_light_pin, on)
        self.light_on = on
        self.is_flashing = False

    def flash_light(self, flash_length=0.5):
        self.flash_length = flash_length
        self.is_flashing = True
        self.set_light(True)
        self.next_flash = time.time() + flash_length

    def tick(self):
        now = time.time()
        if self.is_flashing and now >= self.next_flash:
            self.set_light(not self.light_on)
            self.next_flash = now + self.flash_length


