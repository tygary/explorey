import random
import time

from lighting.Light import Light
from lighting.routines.BleuRoutine import LIGHT_UNSET, LIGHT_FADE, LIGHT_BLINK, MAIN_COLOR, ACCENT_COLOR_1, \
    ACCENT_COLOR_2, ACCENT_COLOR_3
from lighting.routines.Routine import Routine


class MushroomRoutine(Routine):
    now = None

    cave_panel_lights = None

    cavePanelCurrentColor = [0, 0, 255]
    cavePanelNextColor = [0, 0, 255]
    cavePanelFlashColor = [0, 0, 0]
    cavePanelColorTimestamp = 0
    cavePanelColorDuration = 0
    cavePanelColorSchemeIndex = 0
    cavePanelColorSchemeIndexNew = 0
    cavePanelColorTransitioning = False

    cavePanelColorSchemes = [
        [[0, 81, 140], [0, 164, 229], [0, 61, 81], [0, 162, 216]],  # blues
        [
            [63, 168, 204],
            [117, 86, 124],
            [207, 255, 145],
            [109, 249, 186],
        ],  # blue green purple
        [
            [189, 51, 7],
            [235, 161, 11],
            [140, 163, 8],
            [242, 187, 12],
        ],  # red orange yellow green
        [[160, 26, 125], [49, 24, 71], [236, 64, 103], [239, 93, 96]],  # pinks
        [
            [15, 163, 177],
            [247, 160, 114],
            [237, 222, 164],
            [255, 155, 66],
        ],  # blue orange yellow
        [
            [178, 247, 239],
            [247, 214, 224],
            [123, 223, 242],
            [242, 181, 212],
        ],  # cotton candy
        [[178, 255, 158], [29, 211, 176], [60, 22, 66], [175, 252, 65]],  # greens
    ]

    def __init__(self, pixels, addresses, should_override=False, brightness=1.0):
        Routine.__init__(self, pixels, addresses, should_override, brightness)
        self.cave_panel_lights = [Light] * len(addresses)
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
                print("light fade")
                if light.wait:
                    print("Light waiting")
                    if self.now > (light.timestamp + light.waitDuration):
                        light.wait = False
                        light.timestamp = self.now
                        light.nextActionTime = light.timestamp + light.duration
                elif light.up:

                    def onFinishIncrement():
                        self.pickNewLightMode(light)

                    light.on_finish = onFinishIncrement
                    Light.increment_color(light, self.now)
                    print("incrementing color")
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
        if rand < 50:
            light.freq_mode = LIGHT_UNSET
            light.wait = True
            light.timestamp = self.now
            light.currentValue = [0, 0, 0]
            light.waitDuration = random.randrange(4000, 20000)
        elif rand > 90:
            light.freq_mode = LIGHT_BLINK
        else:
            light.freq_mode = LIGHT_FADE

        if light.freq_mode == LIGHT_FADE:
            print("Got light fde")
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
        elif light.freq_mode == LIGHT_BLINK:
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
