import RPi.GPIO as GPIO
import time

from timemachine.Button import Button
from lighting.routines import Routines

DEBOUNCE_TIME = 0.2


BUTTON_NONE = -1
BUTTON_UP = 0
BUTTON_ONE = 1
BUTTON_TWO = 2
BUTTON_THREE = 3
BUTTON_FOUR = 4
BUTTON_FIVE = 5
BUTTON_SIX = 6
BUTTON_DOWN = 7


class ElevatorButtons(object):
    last_button_press = 0
    a = 0
    b = 0
    c = 0
    d = 0

    def __init__(self, pins, callback):
        self.pins = pins
        self.callback = callback

        self.button_a = Button(self.pins[0], callback=self._on_button_pressed)
        self.button_b = Button(self.pins[1], callback=self._on_button_pressed)
        self.button_c = Button(self.pins[2], callback=self._on_button_pressed)
        self.button_d = Button(self.pins[3], callback=self._on_button_pressed)

    def _on_button_pressed(self):
        # now = time.time()
        # if now - self.last_button_press > DEBOUNCE_TIME:
        # self.last_button_press = now
        old_a = self.a
        old_b = self.b
        old_c = self.c
        old_d = self.d
        self.a = GPIO.input(self.pins[0])
        self.b = GPIO.input(self.pins[1])
        self.c = GPIO.input(self.pins[2])
        self.d = GPIO.input(self.pins[3])
        if self.a != old_a or self.b != old_b or self.c != old_c or self.d != old_d:
            print("Elevator Button Pressed: ", self.a, self.b, self.c)
            self._update_mode()
            self.callback(self.mode)

    def _update_mode(self):
        if self.a == 0:
            self.mode = BUTTON_ONE
            print("Elevator Button One Pressed")
        elif self.b == 0:
            self.mode = BUTTON_THREE
            print("Elevator Button Three Pressed")
        elif self.c == 0:
            self.mode = BUTTON_FOUR
            print("Elevator Button Four Pressed")
        elif self.d == 0:
            self.mode = BUTTON_UP
            print("Elevator Button Up Pressed")
        else:
            self.mode = BUTTON_NONE
        # if self.a == 1 and self.b == 1 and self.c == 1 and self.d == 1:
        #     self.mode = BUTTON_NONE
        # if self.a == 0 and self.b == 1 and self.c == 1 and self.d == 1:
        #     self.mode = BUTTON_UP
        # if self.a == 1 and self.b == 0 and self.c == 1 and self.d == 1:
        #     self.mode = BUTTON_ONE
        # if self.a == 0 and self.b == 0 and self.c == 1 and self.d == 1:
        #     self.mode = BUTTON_TWO
        # if self.a == 1 and self.b == 1 and self.c == 0 and self.d == 1:
        #     self.mode = BUTTON_THREE
        # if self.a == 0 and self.b == 1 and self.c == 0 and self.d == 1:
        #     self.mode = BUTTON_FOUR
        # if self.a == 1 and self.b == 0 and self.c == 0 and self.d == 1:
        #     self.mode = BUTTON_FIVE
        # if self.a == 0 and self.b == 0 and self.c == 0 and self.d == 1:
        #     self.mode = BUTTON_SIX
        # if self.a == 1 and self.b == 1 and self.c == 1 and self.d == 0:
        #     self.mode = BUTTON_DOWN


class GameElevatorButtons(ElevatorButtons):
    def __init__(self, pixels, pins, button_lights, callback):
        super().__init__(pins, callback)
        self.pixels = pixels
        self.button_lights = button_lights
        self.desired_button = -1
        self.completed = False
        self.party_mode = False
        self._update_lights()

    def _update_lights(self):
        if self.party_mode:
            self.routines = [Routines.RainbowRoutine(self.pixels, [light]) for light in self.button_lights]
        else:
            self.routines = [Routines.BlackoutRoutine(self.pixels, [light]) for light in self.button_lights]
            if self.desired_button > -1 and not self.completed:
                self.routines[self.desired_button] = Routines.RainbowRoutine(self.pixels, [self.button_lights[self.desired_button]])

    def _on_button_pressed(self):
        super()._on_button_pressed()
        if self.desired_button > -1 and self.mode == self.desired_button:
            self.desired_button = BUTTON_NONE
            self.completed = True
            self._update_lights()
            self.callback(self.mode)

    def set_desired_button(self, button):
        self.desired_button = button
        self.completed = False
        self._update_lights()

    def set_party_mode(self):
        self.party_mode = True
        self._update_lights()

    def off(self):
        self.desired_button = BUTTON_NONE
        self.completed = True
        self.party_mode = False
        self._update_lights()

    def tick(self):
        for routine in self.routines:
            routine.tick()
