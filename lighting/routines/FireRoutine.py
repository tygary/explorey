import random
from random import randint

from lighting.Colors import Colors
from lighting.routines.Routine import Routine

MAX_LED_POWER = 255
MAX_FIRE_POWER = 155
MAX_CHANGE = 5


class FireRoutine(Routine):
    values = []
    colors = [Colors.red]
    pixel_colors = []
    current_power = 0

    def __init__(self, pixels, addresses, colors=None):
        Routine.__init__(self, pixels, addresses)
        if colors:
            self.colors = colors
        for i, address in enumerate(self.addresses):
            self.__register_pixel(i)

    def __register_pixel(self, i):
        self.pixel_colors[i] = random.choice(self.colors)
        self.current_power = randint(0, MAX_FIRE_POWER)
        multiplier = self.current_power / MAX_LED_POWER
        self.values[i] = [
            self.pixel_colors[i][0] * multiplier,
            self.pixel_colors[i][1] * multiplier,
            self.pixel_colors[i][2] * multiplier,
            self.pixel_colors[i][3] * multiplier
        ]

    def update_addresses(self, updated_addresses):
        old_values = self.values
        old_pixel_colors = self.pixel_colors
        self.addresses = updated_addresses
        self.values = []
        self.pixel_colors = []
        for i, address in enumerate(updated_addresses):
            if old_values[i]:
                self.values[i] = old_values[i]
                self.pixel_colors[i] = old_pixel_colors[i]
            else:
                self.__register_pixel(i)

    def tick(self):
        for i, address in enumerate(self.addresses):
            self.current_power = (self.current_power + randint(0, MAX_CHANGE)) % MAX_FIRE_POWER
            multiplier = self.current_power / MAX_LED_POWER
            self.values[i] = [
                self.pixel_colors[i][0] * multiplier,
                self.pixel_colors[i][1] * multiplier,
                self.pixel_colors[i][2] * multiplier,
                self.pixel_colors[i][3] * multiplier
            ]
            self.pixels.setRGBW(address, self.values[i])
