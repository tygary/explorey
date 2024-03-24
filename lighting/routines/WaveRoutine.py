from random import randrange

from lighting.Light import Light
from lighting.routines.BleuRoutine import LIGHT_FADE
from lighting.routines.TimeRoutine import TimeRoutine


class WaveRoutine(TimeRoutine):
    next_action = 0
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

    def __init__(
        self,
        pixels,
        addresses,
        colors,
        starting_color=None,
        delay=0,
        wave_wait_time=10000,
    ):
        TimeRoutine.__init__(self, pixels, addresses)
        self.colors = colors[:]
        self.lights = []
        self.delay = delay
        self.wave_wait_time = wave_wait_time
        if starting_color:
            self.starting_color = starting_color[:]
        else:
            self.starting_color = [0, 0, 0, 0]
        for address in enumerate(addresses):
            self.__initialize_light(address)

    def __initialize_light(self, address):
        light = Light(address)
        self.lights.append(light)
        light.intendedColor = self.starting_color[:]
        light.currentValue = self.starting_color[:]
        print("initialized light ", address, light.intendedColor)

    def update_addresses(self, addresses):
        TimeRoutine.update_addresses(self, addresses)
        old_lights = self.lights
        self.lights = []
        for i, address in enumerate(addresses):
            if old_lights[i]:
                self.lights.append(old_lights[i])
            else:
                self.__initialize_light(address)

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
