import random
import time

from lighting.Light import Light
from lighting.routines.BleuRoutine import LIGHT_UNSET, LIGHT_FADE, LIGHT_BLINK, MAIN_COLOR, ACCENT_COLOR_1, \
    ACCENT_COLOR_2, ACCENT_COLOR_3, CAVE_COLOR_SCHEME_BLUES, CAVE_COLOR_SCHEME_BLUE_GREEN_PURPLE, \
    CAVE_COLOR_SCHCME_RED_ORANGE_YELLOW_GREEN, CAVE_COLOR_SCHEME_PINKS, CAVE_COLOR_SCHEME_BLUE_ORANGE_YELLOW, \
    CAVE_COLOR_SCHEME_COTTON_CANDY, CAVE_COLOR_SCHEME_GREENS
from lighting.routines.Routine import Routine


class MushroomRoutine(Routine):
    def __init__(self, pixels, addresses, should_override=False, brightness=1.0, color_schemes=None):
        Routine.__init__(self, pixels, addresses, should_override, brightness)

        self.now = None
        self.cavePanelCurrentColor = [0, 0, 255]
        self.cavePanelNextColor = [0, 0, 255]
        self.cavePanelFlashColor = [0, 0, 0]
        self.cavePanelColorTimestamp = 0
        self.cavePanelColorDuration = 0
        self.cavePanelColorSchemeIndex = 0
        self.cavePanelColorSchemeIndexNew = 0
        self.cavePanelColorTransitioning = False

        self.cavePanelColorSchemes = [
            CAVE_COLOR_SCHEME_BLUES,
            CAVE_COLOR_SCHEME_BLUE_GREEN_PURPLE,
            CAVE_COLOR_SCHCME_RED_ORANGE_YELLOW_GREEN,
            CAVE_COLOR_SCHEME_PINKS,
            CAVE_COLOR_SCHEME_BLUE_ORANGE_YELLOW,
            CAVE_COLOR_SCHEME_COTTON_CANDY,
            CAVE_COLOR_SCHEME_GREENS
        ]

        self.cave_panel_lights = [Light] * len(addresses)
        if color_schemes is not None:
            self.cavePanelColorSchemes = color_schemes
        for i in range(len(addresses)):
            self.cave_panel_lights[i] = Light(addresses[i])

    def tick(self):
        self.now = int(round(time.time() * 1000))
        for i in range(len(self.cave_panel_lights)):
            light = self.cave_panel_lights[i]
            if light.mode == LIGHT_UNSET:
                light.currentValue = [0, 0, 0]
                if light.wait:
                    if self.now > (light.timestamp + light.waitDuration):
                        light.wait = False
                        self.pickNewLightMode(light)
                else:
                    self.pickNewLightMode(light)
            elif light.mode == LIGHT_FADE:
                if light.wait:
                    if self.now > (light.timestamp + light.waitDuration):
                        light.wait = False
                        light.timestamp = self.now
                        light.nextActionTime = light.timestamp + light.duration
                elif light.up:

                    def onFinishIncrement():
                        self.pickNewLightMode(light)

                    light.on_finish = onFinishIncrement
                    Light.increment_color(light, self.now)
                #    self.setNewIncrementingLightColor(light)
                else:

                    def onFinishDecrement():
                        self.pickNewLightMode(light)
                    light.on_finish = onFinishDecrement
                    Light.decrement_color(light, self.now)
            #
            elif light.mode == LIGHT_BLINK:
                if self.now > light.nextActionTime:
                    if light.on:
                        light.currentValue = light.previousColor
                        light.on = False
                        light.iterations += -1

                        if light.iterations == 0:
                            self.pickNewLightMode(light)
                    else:
                        light.currentValue = light.intendedColor
                        light.on = True
                    light.timestamp = self.now
                    light.nextActionTime = light.timestamp + light.duration
            self.pixels.setColor(light.address, light.currentValue)

    def pickNewLightMode(self, light):
        rand = random.randrange(0, 100)
        if rand < 70:
            light.mode = LIGHT_UNSET
            light.wait = True
            light.timestamp = self.now
            light.currentValue = [0, 0, 0]
            light.waitDuration = random.randrange(4000, 20000)
        elif rand > 95:
            light.mode = LIGHT_BLINK
        else:
            light.mode = LIGHT_FADE

        if light.mode == LIGHT_FADE:
            colorBias = random.randrange(0, 1000)
            colorIndex = 0
            breakNum1 = 700
            breakNum2 = 900
            if colorBias < breakNum1:
                colorIndex = MAIN_COLOR
            elif colorBias >= breakNum1 and colorBias < breakNum2:
                colorIndex = ACCENT_COLOR_1
            else:
                colorIndex = ACCENT_COLOR_2
            light.currentValue = [0, 0, 0]
            light.intendedColor = self.getNewLightColor(colorIndex)
            light.duration = random.randrange(1000, 7000)
            light.iterations = random.randrange(1, 3)
            light.up = True
            light.timestamp = self.now
            light.nextActionTime = light.timestamp + light.duration
        elif light.mode == LIGHT_BLINK:
            light.intendedColor = self.getNewLightColor(MAIN_COLOR)
            light.previousColor = self.getNewLightColor(ACCENT_COLOR_3)
            light.currentValue = light.previousColor
            light.on = False
            light.timestamp = self.now
            light.iterations = random.randrange(5, 10)
            light.duration = random.randrange(100, 700)

    def getNewLightColor(self, colorIndex):
        if self.now > (self.cavePanelColorTimestamp + self.cavePanelColorDuration):
            if self.cavePanelColorTransitioning:
                print("Finished Transitioning Color Scheme")
                self.cavePanelColorTransitioning = False
                self.cavePanelColorSchemeIndex = self.cavePanelColorSchemeIndexNew
                self.cavePanelColorDuration = random.randrange(8000, 30000)
                self.cavePanelColorTimestamp = self.now
            else:
                self.cavePanelColorTransitioning = True
                self.cavePanelColorSchemeIndexNew = random.randrange(
                    0, len(self.cavePanelColorSchemes)
                )
                self.cavePanelColorDuration = random.randrange(3000, 8000)
                self.cavePanelColorTimestamp = self.now
                print(
                    "Switching to color scheme {}".format(
                        self.cavePanelColorSchemeIndexNew
                    )
                )

        colorScheme = self.cavePanelColorSchemes[self.cavePanelColorSchemeIndex]
        if self.cavePanelColorTransitioning:
            finish_time = self.cavePanelColorTimestamp + self.cavePanelColorDuration
            colorBias = int(
                round(
                    (
                        1.0
                        - (
                            (float(finish_time) - float(self.now))
                            / float(self.cavePanelColorDuration)
                        )
                    )
                    * 1000
                )
            )
            colorChance = random.randrange(0, 1000)
            if colorChance > colorBias:
                colorScheme = self.cavePanelColorSchemes[self.cavePanelColorSchemeIndex]
            else:
                colorScheme = self.cavePanelColorSchemes[
                    self.cavePanelColorSchemeIndexNew
                ]

        return [
            colorScheme[colorIndex][0],
            colorScheme[colorIndex][1],
            colorScheme[colorIndex][2],
        ]
