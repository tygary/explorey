from random import randrange
import time

from lighting.Light import Light
from lighting.routines.BleuRoutine import LIGHT_FADE
from lighting.routines.TimeRoutine import TimeRoutine

WAVE_PIXEL_SPEED = 100


class Wave(object):
    def __init__(self, color, speed, addresses):
        self.color = color
        self.speed = speed
        self.current_index = 0
        self.lights = []
        self.addresses = addresses
        for address in addresses:
            self.lights.append(Light(address))
        self.update_next_event_time()

    def update_next_event_time(self):
        self.next_event_time = time.time() * 1000 + (WAVE_PIXEL_SPEED / self.speed)

    def update_addresses(self, addresses):
        if len(addresses) == len(self.addresses):
            return
        self.addresses = addresses
        light_by_address = {
            light.address: light for light in self.lights
        }

        for i, address in enumerate(addresses):
            if light_by_address.get(address):
                print("reusing light", i, address)
                self.lights.append(light_by_address[address])
            else:
                print("creating new light", i, address)
                self.lights.append(Light(address))


class TriggeredWaveRoutine(TimeRoutine):
    next_action = 0
    pixel_wait_time = 100
    wave_wait_time = 10000
    pixel_fade_time = 1000
    lights = None
    running = True
    delay = 0

    current_waves = []

    def __init__(
        self,
        pixels,
        addresses,
        should_override=False,
        brightness=1.0,
    ):
        super().__init__(pixels, addresses, should_override, brightness)
        self.starting_color = [0, 0, 0, 0]

    def update_addresses(self, addresses):
        super().update_addresses(addresses)
        self.addresses = addresses
        print("Updating addresses")
        for wave in self.current_waves:
            wave.update_addresses(addresses)

    def trigger(self, color, speed=1.0):
        print("Launching Wave")
        self.current_waves.append(Wave(color, speed, self.addresses))

    def tick(self):
        super().tick()
        pixels = [[0, 0, 0] for _ in range(0, len(self.addresses))]
        for wave in self.current_waves:
            if self.now > wave.next_event_time:
                wave.current_index += 1
                if wave.current_index < len(wave.lights):
                    print("Adding index to wave", wave.current_index, wave.speed)
                    light = wave.lights[wave.current_index]
                    print("light address", light.address)
                    light.intendedColor = wave.color[:]
                    light.duration = min(self.pixel_fade_time / wave.speed, 100)
                    light.iterations = randrange(1, 2)
                    light.up = True
                    light.timestamp = self.now
                    light.waitDuration = randrange(10, 100)
                    light.nextActionTime = light.timestamp + light.duration
                    light.mode = LIGHT_FADE
                    wave.update_next_event_time()
                else:
                    is_done = True
                    for light in wave.lights:
                        if light.iterations > 0:
                            is_done = False
                    if is_done:
                        print("removing wave")
                        self.current_waves.remove(wave)
            for i in range(0, len(pixels)):
                if i < len(wave.lights):
                    light = wave.lights[i]
                    Light.update_color(light, self.now)
                    prev_value = pixels[i]
                    pixels[i] = [
                        min(prev_value[0] + light.currentValue[0], 255),
                        min(prev_value[1] + light.currentValue[1], 255),
                        min(prev_value[2] + light.currentValue[2], 255),
                    ]
        print("Updating addresses", self.addresses)
        print("pixels", pixels)
        for i, address in enumerate(self.addresses):
            if i < len(pixels):
                self.pixels.setColor(address, pixels[i])
            # print self.lights[0].currentValue
            # print self.lights[0].nextActionTime - self.now
            # print self.lights[0].iterations
