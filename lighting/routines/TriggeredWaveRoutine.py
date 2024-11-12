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
        for i, address in enumerate(addresses):
            self.lights.append(Light(address))
        self.update_next_event_time()

    def update_next_event_time(self):
        self.next_event_time = time.time() * 1000 + (WAVE_PIXEL_SPEED / self.speed)
    
    def update_addresses(self, addresses):
        old_lights = self.lights
        light_by_address = {
            light.address: light for light in self.lights
        }

        for i, address in enumerate(addresses):
            if i < len(old_lights) and light_by_address.get(address):
                self.lights.append(light_by_address[address])
            else:
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
        TimeRoutine.__init__(self, pixels, addresses, should_override, brightness)
        print("addresses", addresses, len(addresses))
        self.starting_color = [0, 0, 0, 0]

    def update_addresses(self, addresses):
        TimeRoutine.update_addresses(self, addresses)
        for wave in self.current_waves:
            wave.update_addresses(addresses)

    def trigger(self, color, speed=1.0):
        print("Launching Wave")
        self.current_waves.append(Wave(color, speed, self.addresses))

    def tick(self):
        TimeRoutine.tick(self)

        pixels = [[0, 0, 0] for _ in range(0, len(self.addresses))]

        for wave in self.current_waves:
            if self.now > wave.next_event_time:
                wave.current_index += 1
                if wave.current_index < len(wave.lights):
                    print("Adding index to wave", wave.current_index, wave.speed)
                    light = wave.lights[wave.current_index]
                    light.intendedColor = wave.color[:]
                    light.duration = min(self.pixel_fade_time / wave.speed, 100)
                    light.iterations = randrange(1, 3)
                    light.up = True
                    light.timestamp = self.now
                    light.waitDuration = randrange(100, 1000)
                    light.nextActionTime = light.timestamp + light.duration
                    light.mode = LIGHT_FADE
                    wave.update_next_event_time()
                else:
                    print("removing wave")
                    self.current_waves.remove(wave)
            for i in range(0, len(wave.lights)):
                light = wave.lights[i]
                Light.update_color(light, self.now)
                print("Light", i, light.address, light.currentValue)
                print("Pixels", pixels)
                prev_value = pixels[i]
                pixels[i] = [
                    min(prev_value[0] + light.currentValue[0], 255),
                    min(prev_value[1] + light.currentValue[1], 255),
                    min(prev_value[2] + light.currentValue[2], 255),
                ]
        for i, address in enumerate(self.addresses):
            self.pixels.setColor(address, pixels[i])
            # print self.lights[0].currentValue
            # print self.lights[0].nextActionTime - self.now
            # print self.lights[0].iterations
