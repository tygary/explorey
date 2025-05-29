import math

from lighting.routines.TimeRoutine import TimeRoutine


class GaugeRoutine(TimeRoutine):
    color = [255, 0, 0]
    percentage = 0
    prev_breakpoint = 0
    width = 5

    def __init__(self, pixels, addresses, color=[255, 0, 0]):
        super().__init__(pixels, addresses)
        self.color = color

    def update_percentage(self, percentage):
        self.percentage = percentage

    def tick(self):
        num_pixels = len(self.addresses)
        num_pixels_minus_width = num_pixels - self.width
        start_pixel = math.floor(num_pixels_minus_width * self.percentage)
        end_pixel = start_pixel + self.width
        for i in range(0, num_pixels):
            if i >= start_pixel and i < end_pixel:
                self.pixels.setColor(self.addresses[i], self.color)
            else:
                self.pixels.setColor(self.addresses[i], [0, 0, 0])
