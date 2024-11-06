import RPi.GPIO as GPIO
import time

from printer.addeventdetection import add_event_detection
from lighting.routines import Routines
from lighting.Colors import Colors


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

        add_event_detection(self.button_pin, callback=self._on_press, pullup=True)
        if button_light_pin > 0:
            GPIO.setup(self.button_light_pin, GPIO.OUT)

    def _on_press(self, value):
        now = time.time()
        if now > self.waiting:
            self.waiting = time.time() + WAIT_TIME
            if self.callback:
                self.callback()

    def _set_light(self, on):
        if self.button_light_pin > 0:
            GPIO.output(self.button_light_pin, on)
        self.light_on = on

    def set_light(self, on):
        self._set_light(on)
        self.is_flashing = False

    def flash_light(self, flash_length=0.5):
        self.flash_length = flash_length
        self.is_flashing = True
        self._set_light(True)
        self.next_flash = time.time() + flash_length

    def tick(self):
        now = time.time()
        if self.button_light_pin > 0 and self.is_flashing and now >= self.next_flash:
            self._set_light(not self.light_on)
            self.next_flash = now + self.flash_length


class GameButtonWithFourLights(Button):
    def __init__(self, pixels, button_pin, button_light_pixels, callback=None):
        super().__init__(button_pin, -1, callback)
        self.pixels = pixels
        self.button_light_pixels = button_light_pixels
        self.pending = False
        self.completed = False
        self.party_mode = False
        self._update_routine()

    def _update_routine(self):
        if self.party_mode:
            self.routine = Routines.RainbowRoutine(self.pixels, self.button_light_pixels)
        elif self.pending:
            self.routine = Routines.PulseRoutine(self.pixels, self.button_light_pixels, Colors.mid_green)
        else:
            self.routine = Routines.BlackoutRoutine(self.pixels, self.button_light_pixels)

    def _on_press(self, value):
        super()._on_press(value)
        if (self.pending and not self.completed):
            print("Completed Button!")
            self.pending = False
            self.completed = True
            self._update_routine()

    def _set_light(self, on):
        super().__set_light(on)
        self._update_routine()

    def set_pending(self):
        print("Button set pending")
        self.pending = True
        self.completed = False
        self.party_mode = False
        self._update_routine()

    def set_party_mode(self):
        self.pending = False
        self.completed = False
        self.party_mode = True
        self._update_routine()

    def off(self):
        self.pending = False
        self.completed = True
        self.party_mode = False
        self._update_routine()

    def tick(self):
        super().tick()
        self.routine.tick()
