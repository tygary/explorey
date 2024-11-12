import math

from lighting.routines.PulseRoutine import PulseRoutine
from lighting.routines.TimeRoutine import TimeRoutine


class PowerGaugeRoutine(TimeRoutine):
    color = [255, 0, 0]
    percentage = 0
    pulse_routine = None
    prev_breakpoint = 0

    def __init__(self, pixels, addresses, color=[255, 0, 0]):
        super().__init__(self, pixels, addresses)
        self.color = color

    def update_percentage(self, percentage):
        self.percentage = percentage

    def tick(self):
        num_pixels = len(self.addresses)
        if self.percentage is 0:
            for addr in self.addresses:
                self.pixels.setColor(addr, [0, 0, 0])
        else:
            pixel_breakpoint = math.ceil(self.percentage * num_pixels)
            for i in range(0, pixel_breakpoint - 1):
                self.pixels.setColor(self.addresses[i], [255, 0, 0])
            if pixel_breakpoint < num_pixels:
                for i in range(pixel_breakpoint, num_pixels):
                    self.pixels.setColor(self.addresses[i], [0, 0, 0])
            rate = round(((1 - self.percentage) * 0.5 + 0.01) * 100) / 100
            if pixel_breakpoint != self.prev_breakpoint:
                self.prev_breakpoint = pixel_breakpoint

                self.pulse_routine = PulseRoutine(self.pixels, [self.addresses[pixel_breakpoint - 1]], self.color, rate=rate)
            self.pulse_routine.rate = rate
            self.pulse_routine.tick()
