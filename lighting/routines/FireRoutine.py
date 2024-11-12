import random
from random import randint

from lighting.Colors import Colors
from lighting.routines.Routine import Routine

MAX_LED_POWER = 255
MAX_FIRE_POWER = 155
MAX_CHANGE = 5


class FireRoutine(Routine):
    def __init__(self, pixels, addresses, colors=None, should_override=False, brightness=1.0):
        super().__init__(self, pixels, addresses, should_override, brightness)
        self.current_magnitudes = []
        self.values = []
        colors = [Colors.red]
        self.pixel_colors = []
        if colors:
            self.colors = colors
        for i, address in enumerate(self.addresses):
            self.__register_pixel(i)

    def __register_pixel(self, i):
        self.pixel_colors.append(random.choice(self.colors))
        # current_power = randint(0, MAX_FIRE_POWER)
        # multiplier = self.current_power / MAX_LED_POWER
        magnitude = randint(0, MAX_FIRE_POWER)
        self.current_magnitudes.append(magnitude)
        multiplier = magnitude / MAX_FIRE_POWER
        self.values.append([
            round(self.pixel_colors[i][0] * multiplier),
            round(self.pixel_colors[i][1] * multiplier),
            round(self.pixel_colors[i][2] * multiplier),
            round(self.pixel_colors[i][3] * multiplier)
        ])

    def update_addresses(self, updated_addresses):
        old_values = self.values
        old_pixel_colors = self.pixel_colors
        self.addresses = updated_addresses
        self.values = []
        self.pixel_colors = []
        for i, address in enumerate(updated_addresses):
            if i < len(old_values):
                self.values.append(old_values[i])
                self.pixel_colors.append(old_pixel_colors[i])
            else:
                self.__register_pixel(i)

    def tick(self):
        for i, address in enumerate(self.addresses):
            self.current_magnitudes[i] = (self.current_magnitudes[i] + randint(0, 5)) % MAX_FIRE_POWER
            multiplier = self.current_magnitudes[i] / MAX_FIRE_POWER
            self.values[i] = [
                round(self.pixel_colors[i][0] * multiplier),
                round(self.pixel_colors[i][1] * multiplier),
                round(self.pixel_colors[i][2] * multiplier),
                round(self.pixel_colors[i][3] * multiplier)
            ]
            self.pixels.setRGBW(address, self.values[i])
