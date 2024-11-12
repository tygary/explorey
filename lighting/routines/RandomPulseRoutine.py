import random

from lighting.Colors import Colors
from lighting.Light import Light
from lighting.routines.BleuRoutine import LIGHT_FADE
from lighting.routines.TimeRoutine import TimeRoutine


class RandomPulseRoutine(TimeRoutine):
    def __init__(self, pixels, addresses, should_override=False, brightness=1.0):
        TimeRoutine.__init__(self, pixels, addresses, should_override, brightness=brightness)
        self.lights = []
        for address in addresses:
            light = Light(address)
            self.update_light_mode(light)
            self.lights.append(light)

    def update_light_mode(self, light):
        # colorBias = random.randrange(0, 1000)
        # colorIndex = 0
        # breakNum1 = 700
        # breakNum2 = 900
        # if colorBias < breakNum1:
        #     colorIndex = MAIN_COLOR
        # elif colorBias >= breakNum1 and colorBias < breakNum2:
        #     colorIndex = ACCENT_COLOR_1
        # else:
        #     colorIndex = ACCENT_COLOR_2
        def on_finish_mode():
            self.update_light_mode(light)

        light.intendedColor = Colors.light_green
        light.duration = random.randrange(1000, 7000)
        light.iterations = random.randrange(1, 3)
        light.up = True
        light.timestamp = self.now
        light.nextActionTime = light.timestamp + light.duration
        light.freq_mode = LIGHT_FADE
        light.on_finish = on_finish_mode

    def tick(self):
        TimeRoutine.tick(self)
        for light in self.lights:
            Light.update_color(light, self.now)
            self.pixels.setColor(light.address, light.currentValue)
