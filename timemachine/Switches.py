import RPi.GPIO as GPIO
import time

from printer.addeventdetection import add_event_detection
from lighting.routines import Routines


class TwoWaySwitch(object):
    def __init__(self, pin, callback=None):
        self.pin = pin
        self.callback = callback
        add_event_detection(self.pin, bothdirections=True, callback=self._on_toggle, pullup=True)
        self.mode = GPIO.input(self.pin)

    def _on_toggle(self, value):
        new_mode = GPIO.input(self.pin)
        if new_mode != self.mode:
            self.mode = new_mode
            print(f"Switch toggled:{self.mode}")
            if self.callback:
                self.callback(self.mode)


class GameTwoWaySwitch(TwoWaySwitch):
    def __init__(self, pixels, pin, pixel_off, pixel_on, callback=None):
        super().__init__(pin, callback)
        self.pixels = pixels
        self.pixel_on = pixel_on
        self.pixel_off = pixel_off
        self.desired_mode = self.mode
        self.party_mode = False
        self.completed = True
        self._update_lights()

    def _on_toggle(self, value):
        super()._on_toggle(value)
        if self.desired_mode == self.mode:
            self.completed = True
        self._update_lights()

    def _update_lights(self):
        if self.party_mode:
            self.routine_on = Routines.RainbowRoutine(self.pixels, [self.pixel_on])
            self.routine_off = Routines.RainbowRoutine(self.pixels, [self.pixel_off])
        elif self.completed:
            self.routine_on = Routines.BlackoutRoutine(self.pixels, [self.pixel_on])
            self.routine_off = Routines.BlackoutRoutine(self.pixels, [self.pixel_off])
        elif self.mode:
            self.routine_on = Routines.RainbowRoutine(self.pixels, [self.pixel_on])
            self.routine_off = Routines.BlackoutRoutine(self.pixels, [self.pixel_off])
        else:
            self.routine_on = Routines.BlackoutRoutine(self.pixels, [self.pixel_on])
            self.routine_off = Routines.RainbowRoutine(self.pixels, [self.pixel_off])

    def set_desired_mode(self, mode):
        self.desired_mode = mode
        self.completed = False
        self.party_mode = False
        self._update_lights()

    def set_party_mode(self):
        self.party_mode = True
        self._update_lights()

    def off(self):
        self.party_mode = False
        self.completed = True
        self._update_lights()

    def tick(self):
        self.routine_on.tick()
        self.routine_off.tick()


class ThreeWaySwitch(object):
    def __init__(self, pin_a, pin_b, callback=None):
        print("pin_a", pin_a)
        print("pin_b", pin_b)
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.callback = callback

        add_event_detection(self.pin_a, bothdirections=True, callback=self._on_toggle, pullup=True)
        add_event_detection(self.pin_b, bothdirections=True, callback=self._on_toggle, pullup=True)
        self.mode = 2
        self._update_mode()

    def _update_mode(self):
        a = GPIO.input(self.pin_a)
        b = GPIO.input(self.pin_b)
        new_mode = 2
        if a == 0:
            new_mode = 1
        elif b == 0:
            new_mode = 3
        if new_mode != self.mode:
            self.mode = new_mode
            print(f"Switch toggled a:{a}, b:{b}")

    def _on_toggle(self, value):
        old_mode = self.mode
        self._update_mode()
        if self.mode != old_mode and self.callback:
            self.callback(self.mode)


class GameThreeWaySwitch(ThreeWaySwitch):
    def __init__(self, pixels, pin_a, pin_b, top_pixels, bottom_pixels, callback=None):
        super().__init__(pin_a, pin_b, callback)
        self.pixels = pixels
        self.top_pixels = top_pixels
        self.bottom_pixels = bottom_pixels
        self.routine_top = Routines.BlackoutRoutine(self.pixels, top_pixels)
        self.routine_bottom = Routines.BlackoutRoutine(self.pixels, bottom_pixels)

        self.desired_mode = self.mode
        self.completed = True
        self.party_mode = False

    def _on_toggle(self, value):
        super()._on_toggle(value)
        if self.desired_mode == self.mode or self.completed:
            self.completed = True
            print("Switch is completed!")
        self._update_lights()

    def _update_lights(self):
        if self.party_mode:
            self.routine_top = Routines.RainbowRoutine(self.pixels, self.top_pixels)
            self.routine_bottom = Routines.RainbowRoutine(self.pixels, self.bottom_pixels)
        elif self.completed:
            self.routine_top = Routines.BlackoutRoutine(self.pixels, self.top_pixels)
            self.routine_bottom = Routines.BlackoutRoutine(self.pixels, self.bottom_pixels)
        elif self.desired_mode == 1:
            self.routine_top = Routines.RainbowRoutine(self.pixels, self.top_pixels)
            self.routine_bottom = Routines.BlackoutRoutine(self.pixels, self.bottom_pixels)
        elif self.desired_mode == 3:
            self.routine_top = Routines.BlackoutRoutine(self.pixels, self.top_pixels)
            self.routine_bottom = Routines.RainbowRoutine(self.pixels, self.bottom_pixels)

    def set_desired_mode(self, mode):
        self.desired_mode = mode
        self.completed = False
        print("Power switch desired mode set to", mode)
        self._update_lights()

    def set_party_mode(self):
        self.party_mode = True
        self._update_lights()
    
    def off(self):
        self.party_mode = False
        self.completed = True
        self._update_lights()

    def tick(self):
        self.routine_top.tick()
        self.routine_bottom.tick()
