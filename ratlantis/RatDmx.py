import time
import random
from lighting.DmxControl import DmxControl


LIGHT_ONE = 1
LIGHT_TWO = 6
LIGHT_THREE = 11
LIGHT_FOUR = 16
FOUR_BAR_FLEX = 21

PINK = [232, 60, 239]
PURPLE = [183, 30, 218]
ORANGE = [236, 153, 92]
RED = [247, 5, 10]
BLUE = [15, 100, 255]

UP = True
DOWN = False

AMBIENT = 0
STARTUP = 1
RUNNING = 2

FADE_DURATION = 2


def scale_color(color, scale):
    return [int(color[0] * scale), int(color[1] * scale), int(color[2] * scale)]


class RatDmx(object):
    dmx = DmxControl()

    mode = AMBIENT

    ambient_colors = [scale_color(PINK, 0.6), scale_color(PURPLE, 0.6), scale_color(ORANGE, 0.6), scale_color(BLUE, 0.6)]
    lights = [LIGHT_ONE, LIGHT_TWO, LIGHT_THREE, LIGHT_FOUR]
    light_directions = [UP, UP, UP, UP]
    light_values = [1, 1, 1, 1]
    next_event_time = 0

    def __init__(self):
        self.__set_ambient()

    def __set_ambient(self):
        for index in range(0, len(self.lights)):
            self.dmx.setParCan(self.lights[index], self.ambient_colors[index])
        self.dmx.set4barFlex(FOUR_BAR_FLEX, [
            self.ambient_colors[0],
            self.ambient_colors[1],
            self.ambient_colors[2],
            self.ambient_colors[3]
        ])
        self.mode = AMBIENT
        print("Starting Ambient DMX")

    def __startup(self):
        self.light_values = [0, 0.33, 0.66, 0.99]
        for index in range(0, len(self.lights)):
            self.dmx.setParCan(self.lights[index], scale_color(RED, self.light_values[index]))
        self.dmx.set4barFlex(FOUR_BAR_FLEX, [
            scale_color(RED, self.light_values[0]),
            scale_color(RED, self.light_values[1]),
            scale_color(RED, self.light_values[2]),
            scale_color(RED, self.light_values[3])
        ])
        self.mode = STARTUP
        self.prev_event = time.time()
        print("Starting Startup DMX")

    def __running(self):
        for index in range(0, len(self.lights)):
            self.dmx.setParCan(self.lights[index], scale_color(RED, 0.1))
        self.dmx.set4barFlex(FOUR_BAR_FLEX, [
            scale_color(RED, 0.1),
            scale_color(RED, 0.1),
            scale_color(RED, 0.1),
            scale_color(RED, 0.1)
        ])
        self.mode = RUNNING
        print("Starting Running DMX")

    def change_mode(self, active, startup):
        if startup and not self.mode == STARTUP:
            self.__startup()
        elif active and not self.mode == RUNNING:
            self.__running()
        elif not startup and not active and not self.mode == AMBIENT:
            self.__set_ambient()

    def update(self):
        if self.mode == STARTUP:
            for index in range(0, len(self.lights)):
                self.light_values[index] = self.light_values[index] + (random.random() * 0.2 * (-1 if self.light_directions[index] is DOWN else 1))
                if self.light_values[index] > 1:
                    self.light_values[index] = 1
                    self.light_directions[index] = not self.light_directions[index]
                elif self.light_values[index] < 0:
                    self.light_values[index] = 0
                    self.light_directions[index] = not self.light_directions[index]
                # print(f"Updating Light {self.lights[index]} - {scale_color(RED, self.light_values[index])}")
                self.dmx.setParCan(self.lights[index], scale_color(RED, self.light_values[index]))
            self.dmx.set4barFlex(FOUR_BAR_FLEX, [
                scale_color(RED, self.light_values[0]),
                scale_color(RED, self.light_values[1]),
                scale_color(RED, self.light_values[2]),
                scale_color(RED, self.light_values[3])
            ])
        self.dmx.render()
