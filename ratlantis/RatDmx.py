import time
import random
from lighting.DmxControl import DmxControl


LIGHT_ONE = 1
LIGHT_TWO = 6
LIGHT_THREE = 11
LIGHT_FOUR = 16
FOUR_BAR_FLEX = 21
DIMMER_SPOTS = [66, 67]
UNUSED_DIMMER = [65, 68]

PINK = [232, 60, 239]
PURPLE = [183, 30, 218]
ORANGE = [236, 153, 92]
RED = [247, 5, 10]
BLUE = [15, 100, 255]

ALL_COLORS = [RED, BLUE, ORANGE, PINK, PURPLE]

UP = True
DOWN = False

AMBIENT = 0
STARTUP = 1
RUNNING = 2
FINALE = 3

FADE_DURATION = 2


def scale_color(color, scale):
    return [int(color[0] * scale), int(color[1] * scale), int(color[2] * scale)]


class RatDmx(object):
    dmx = DmxControl()

    mode = AMBIENT

    ambient_colors = [scale_color(PINK, 0.6), scale_color(PURPLE, 0.6), scale_color(ORANGE, 0.6), scale_color(BLUE, 0.6)]
    lights = [LIGHT_ONE, LIGHT_TWO, LIGHT_THREE, LIGHT_FOUR]
    light_directions = [UP, UP, UP, UP]
    light_colors = [RED, RED, RED, RED]
    light_values = [1, 1, 1, 1]
    next_event_time = 0
    dimmer_directions = [UP, DOWN]
    dimmer_values = [0, 100]
    available_colors = [RED]

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
        for addr in DIMMER_SPOTS + UNUSED_DIMMER:
            self.dmx.setDimmer(addr, 0)
        self.mode = AMBIENT
        print("Starting Ambient DMX")

    def __startup(self):
        self.light_values = [0, 0.33, 0.66, 0.99]
        self.light_colors = [RED, RED, RED, RED]
        self.available_colors = [RED]
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

    def __finale(self):
        self.mode = FINALE
        print("Starting dmx finale")
        self.available_colors = ALL_COLORS
        self.dmx.setDimmer(DIMMER_SPOTS[0], self.dimmer_values[0])
        self.dmx.setDimmer(DIMMER_SPOTS[1], self.dimmer_values[1])

    def change_mode(self, active, startup, finale=False):
        print("DMX changemode")
        if finale and not self.mode == FINALE:
            self.__finale()
        elif startup and not self.mode == STARTUP:
            self.__startup()
        elif active and not self.mode == RUNNING:
            self.__running()
        elif not startup and not active and not self.mode == AMBIENT:
            self.__set_ambient()

    def update(self):
        if self.mode == STARTUP or self.mode == FINALE:
            for index in range(0, len(self.lights)):
                self.light_values[index] = self.light_values[index] + (random.random() * 0.2 * (-1 if self.light_directions[index] is DOWN else 1))
                if self.light_values[index] > 1:
                    self.light_values[index] = 1
                    self.light_directions[index] = not self.light_directions[index]
                elif self.light_values[index] < 0:
                    self.light_values[index] = 0
                    self.light_directions[index] = not self.light_directions[index]
                    self.light_colors[index] = random.choice(self.available_colors)
                # print(f"Updating Light {self.lights[index]} - {scale_color(RED, self.light_values[index])}")
                self.dmx.setParCan(self.lights[index], scale_color(RED, self.light_values[index]))
            self.dmx.set4barFlex(FOUR_BAR_FLEX, [
                scale_color(self.light_colors[0], self.light_values[0]),
                scale_color(self.light_colors[1], self.light_values[1]),
                scale_color(self.light_colors[2], self.light_values[2]),
                scale_color(self.light_colors[3], self.light_values[3])
            ])
        if self.mode == FINALE:
            for index in range(0, len(self.dimmer_values)):
        #         self.dimmer_values[index] = self.dimmer_values[index] + (random.random() * 5 * (-1 if self.dimmer_directions[index] is DOWN else 1))
        #         if self.dimmer_values[index] > 100:
        #             self.dimmer_values[index] = 100
        #             self.dimmer_directions[index] = not self.dimmer_directions[index]
        #         elif self.dimmer_values[index] < 0:
        #             self.dimmer_values[index] = 0
        #             self.dimmer_directions[index] = not self.dimmer_directions[index]
                self.dmx.setDimmer(DIMMER_SPOTS[index], 255)
        self.dmx.render()
