import time

from lighting.DmxControl import DmxControl


LIGHT_ONE = 1
LIGHT_TWO = 6
LIGHT_THREE = 11
LIGHT_FOUR = 16

PINK = [232, 209, 239]
PURPLE = [183, 109, 218]
ORANGE = [236, 103, 32]
RED = [247, 36, 24]
BLUE = [68, 231, 198]

UP = True
DOWN = False

AMBIENT = 0
STARTUP = 1
RUNNING = 2

FADE_DURATION = 2


def scale_color(color, scale):
    return [int(color[0] * scale), int(color[1] * scale), int(color[2] * scale)]


class TimeDmx(object):
    dmx = DmxControl()

    mode = AMBIENT

    ambient_colors = [PINK, PURPLE, ORANGE, BLUE]
    lights = [LIGHT_ONE, LIGHT_TWO, LIGHT_THREE, LIGHT_FOUR]
    light_directions = [UP, UP, UP, UP]
    light_values = [1, 1, 1, 1]
    next_event_time = 0

    def __init__(self):
        self.__set_ambient()

    def __set_ambient(self):
        for index in range(0, len(self.lights)):
            self.dmx.setParCan(self.lights[index], self.ambient_colors[index])
        self.mode = AMBIENT
        print("Starting Ambient DMX")

    def __startup(self):
        self.light_values = [0, 0.33, 0.66, 0.99]
        for index in range(0, len(self.lights)):
            self.dmx.setParCan(self.lights[index], scale_color(RED, self.light_values[index]))
        self.mode = STARTUP
        self.prev_event = time.time()
        print("Starting Startup DMX")

    def __running(self):
        for index in range(0, len(self.lights)):
            self.dmx.setParCan(self.lights[index], scale_color(RED, 0.2))
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
        if self.mode == RUNNING:
            for index in range(0, len(self.lights)):
                self.light_values[index] = self.light_values[index] + (0.05 * (-1 if self.light_directions[index] is DOWN else 1))
                if self.light_values[index] > 1:
                    self.light_values[index] = 1
                    self.light_directions[index] = not self.light_directions[index]
                elif self.light_values[index] < 0:
                    self.light_values[index] = 0
                    self.light_directions[index] = not self.light_directions[index]
                self.dmx.setParCan(self.lights[index], scale_color(RED, int(self.light_values[index])))
        self.dmx.render()
