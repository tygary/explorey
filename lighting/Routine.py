from random import randint, randrange
import time, math
from lighting.Light import Light, LIGHT_FADE
import random
from lighting.Colors import Colors


class Routine(object):
    addresses = []
    pixels = None

    def __init__(self, pixels, addresses):
        self.pixels = pixels
        self.addresses = addresses

    def tick(self):
        print("tick")


class TimeRoutine(Routine):
    now = None

    def __init__(self, pixels, addresses):
        Routine.__init__(self, pixels, addresses)
        self.update_now()

    def tick(self):
        self.update_now()

    def update_now(self):
        self.now = int(round(time.time() * 1000))


class RandomPulseRoutine(TimeRoutine):
    lights = []

    def __init__(self, pixels, addresses):
        TimeRoutine.__init__(self, pixels, addresses)
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
        light.mode = LIGHT_FADE
        light.on_finish = on_finish_mode

    def tick(self):
        TimeRoutine.tick(self)
        for light in self.lights:
            Light.update_color(light, self.now)
            self.pixels.setColor(light.address, light.currentValue)


class RainbowRoutine(Routine):
    values = {}

    def __init__(self, pixels, addresses):
        Routine.__init__(self, pixels, addresses)
        for i in self.addresses:
            red = 100 + i % 255
            green = i % 255
            blue = 200 + i % 255
            self.values[i] = [red, green, blue]

    def tick(self):
        for i in self.addresses:
            for j in range(2):
                self.values[i][j] = (self.values[i][j] + 5) % 255
            self.pixels.setColor(i, self.values[i])


class FireRoutine(Routine):
    values = {}

    def __init__(self, pixels, addresses):
        Routine.__init__(self, pixels, addresses)
        for i in self.addresses:
            red = randint(0, 155)
            green = 0
            blue = 0
            white = 0
            self.values[i] = [red, green, blue, white]

    def tick(self):
        for i in self.addresses:
            self.values[i][0] = (self.values[i][0] + randint(0, 5)) % 150
            self.pixels.setRGBW(i, self.values[i])


class WaveRoutine(TimeRoutine):
    next_action = None
    pixel_wait_time = 100
    wave_wait_time = 10000
    pixel_fade_time = 1000
    colors = None
    color_index = 0
    starting_color = None
    lights = None
    next_index = 0
    running = True
    delay = 0

    def __init__(self, pixels, addresses, colors, starting_color=None, delay=0):
        Routine.__init__(self, pixels, addresses)
        self.colors = colors[:]
        self.lights = []
        self.delay = delay
        if starting_color:
            self.starting_color = starting_color[:]
        else:
            self.starting_color = [0, 0, 0, 0]
        for address in addresses:
            light = Light(address)
            self.lights.append(light)
            light.intendedColor = self.starting_color[:]
            light.currentValue = self.starting_color[:]

    def tick(self):
        TimeRoutine.tick(self)
        if self.running:
            if self.delay > 0:
                self.next_action = self.now + self.delay
                self.delay = 0
            if self.now > self.next_action:
                # print "action {}".format(self.next_index)
                self.next_action = self.now + self.pixel_wait_time
                if self.next_index < len(self.lights):
                    light = self.lights[self.next_index]
                    light.intendedColor = self.colors[self.color_index][:]
                    light.duration = self.pixel_fade_time
                    light.iterations = randrange(5)
                    light.up = True
                    light.timestamp = self.now
                    light.waitDuration = randrange(1000, 3000)
                    light.nextActionTime = light.timestamp + light.duration
                    light.mode = LIGHT_FADE
                    self.next_index += 1
                else:
                    self.next_index = 0
                    self.next_action = self.now + self.wave_wait_time
                    self.color_index = randrange(len(self.colors))
                    random_chance = randrange(0, 100)
                    if random_chance < 20:
                        self.lights.reverse()
                    # if self.color_index is len(self.colors):
                    #     self.color_index = 0

            for light in self.lights:
                Light.update_color(light, self.now)
                self.pixels.setColor(light.address, light.currentValue)
            # print self.lights[0].currentValue
            # print self.lights[0].nextActionTime - self.now
            # print self.lights[0].iterations


class PulseRoutine(Routine):
    going_up = True
    color = None
    ratio = 0
    values = {}
    rate = 0.05

    def __init__(self, pixels, addresses, color, rate=0.05):
        Routine.__init__(self, pixels, addresses)
        self.color = color
        self.rate = rate
        for i in self.addresses:
            red = 0
            green = 0
            blue = 0
            white = 0
            self.values[i] = [red, green, blue, white]

    def tick(self):
        if self.ratio >= 1:
            self.going_up = False
        if self.ratio <= 0:
            self.going_up = True
        if self.going_up:
            self.ratio += self.rate
        else:
            self.ratio -= self.rate

        for i in self.addresses:
            self.values[i][0] = int(self.ratio * self.color[0])
            self.values[i][1] = int(self.ratio * self.color[1])
            self.values[i][2] = int(self.ratio * self.color[2])
            self.values[i][3] = int(self.ratio * self.color[3])
            self.pixels.setRGBW(i, self.values[i])


class MultiRoutine(Routine):
    routines = []

    def __init__(self, routines):
        Routine.__init__(self, None, [])
        self.routines = routines
        for routine in self.routines:
            print(routine.addresses)

    def tick(self):
        for routine in self.routines:
            routine.tick()


LIGHT_UNSET = -1
LIGHT_FADE = 0
LIGHT_BLINK = 1
LIGHT_NUM_EFFECTS = 2

class BleuRoutine(Routine):

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
        [[63, 168, 204], [117, 86, 124], [207, 255, 145], [109, 249, 186]],  # blue green purple
        [[189, 51, 7], [235, 161, 11], [140, 163, 8], [242, 187, 12]],  # red orange yellow green
        [[160, 26, 125], [49, 24, 71], [236, 64, 103], [239, 93, 96]],  # pinks
        [[15, 163, 177], [247, 160, 114], [237, 222, 164], [255, 155, 66]],  # blue orange yellow
        [[178, 247, 239], [247, 214, 224], [123, 223, 242], [242, 181, 212]],  # cotton candy
        [[178, 255, 158], [29, 211, 176], [60, 22, 66], [175, 252, 65]],  # greens
    ]

    def __init__(self, pixels, addresses):
        Routine.__init__(self, pixels, addresses)

    def tick(self):
        for i in range(len(self.pixels)):
            light = self.pixels[i]
            if light.mode == LIGHT_UNSET:
                self.pickNewLightMode(light)
            if light.mode == LIGHT_FADE:
                if light.wait:
                    if self.now > (light.timestamp + light.waitDuration):
                        light.wait = False
                        light.timestamp = self.now
                elif light.up:
                    def onFinishIncrement():
                        self.pickNewLightMode(light)
                    light.on_finish = onFinishIncrement
                    light.incrementColor(self.now)
                #    self.setNewIncrementingLightColor(light)
                else:
                    def onFinishDecrement():
                        self.pickNewLightMode(light)
                    light.on_finish = onFinishDecrement
                    light.decrementColor(self.now)
                    self.setNewDecrementingLightColor(light)
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
#             self.pixel.setColor(light.address, light.currentValue)

    def pickNewLightMode(self, light):
        rand = random.randrange(0, 100)
        if rand > 90:
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
            light.iterations = random.randrange(5, 10)
            light.timestamp = self.now
            light.duration = random.randrange(100, 700)

    def getNewLightColor(self, colorIndex):
        if self.now > (self.cavePanelColorTimestamp + self.cavePanelColorDuration):
            if self.cavePanelColorTransitioning:
                print "Finished Transitioning Color Scheme"
                self.cavePanelColorTransitioning = False
                self.cavePanelColorSchemeIndex = self.cavePanelColorSchemeIndexNew
                self.cavePanelColorDuration = random.randrange(8000, 30000)
                self.cavePanelColorTimestamp = self.now
            else:
                self.cavePanelColorTransitioning = True
                self.cavePanelColorSchemeIndexNew = random.randrange(0, len(self.cavePanelColorSchemes))
                self.cavePanelColorDuration = random.randrange(3000, 8000)
                self.cavePanelColorTimestamp = self.now
                print "Switching to color scheme {}".format(self.cavePanelColorSchemeIndexNew)

        colorScheme = self.cavePanelColorSchemes[self.cavePanelColorSchemeIndex]
        if self.cavePanelColorTransitioning:
            finish_time = self.cavePanelColorTimestamp + self.cavePanelColorDuration
            colorBias = int(round((1.0 - ((float(finish_time) - float(self.now)) / float(self.cavePanelColorDuration))) * 1000))
            colorChance = random.randrange(0, 1000)
            if colorChance > colorBias:
                colorScheme = self.cavePanelColorSchemes[self.cavePanelColorSchemeIndex]
            else:
                colorScheme = self.cavePanelColorSchemes[self.cavePanelColorSchemeIndexNew]

        return colorScheme[colorIndex]