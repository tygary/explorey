import random

from lighting.routines.TimeRoutine import TimeRoutine


class SpeedGaugeRoutine(TimeRoutine):
    color = [255, 0, 0]
    magnitude = 0
    active = False

    def __init__(self, pixels, addresses, color=[255, 0, 0]):
        TimeRoutine.__init__(pixels, addresses)
        self.color = color

    def update_active(self, active):
        self.active = active

    def update_magnitude(self, magnitude):
        if abs(magnitude) < 50:
            magnitude = 0
        self.magnitude = magnitude

    def tick(self):
        if self.active is False:
            for addr in self.addresses:
                self.pixels.setColor(addr, [0, 0, 0])
            return
        if self.magnitude is 0:
            color = [100, 100, 100]
            self.pixels.setColor(self.addresses[0], color)
        elif self.magnitude > 0:
            color = [255, 0, 0]
        else:
            color = [0, 0, 255]

        abs_mag = abs(self.magnitude)
        num_pixels = len(self.addresses)

        if abs_mag >= 950: # MAX
            pixel_breakpoint = 8
        elif abs_mag >= 900: # Decades
            pixel_breakpoint = 7
        elif abs_mag >= 800: # Years
            pixel_breakpoint = 6
        elif abs_mag >= 700: # Months
            pixel_breakpoint = 5
        elif abs_mag >= 600: # Days
            pixel_breakpoint = 4
        elif abs_mag >= 500: # Hours
            pixel_breakpoint = 3
        elif abs_mag >= 350: # Minutes
            pixel_breakpoint = 2
        elif abs_mag > 100: # Seconds
            pixel_breakpoint = 1
        else: # Frozen
            pixel_breakpoint = 0
        # print(f"Light Magnitude {self.magnitude} - Pixels {on_pixels}")

        # pixel_breakpoint = math.ceil((abs_mag / 1000) * (num_pixels - 1))
        for i in range(0, pixel_breakpoint + 1):
            strength = (random.random() * self.magnitude * 5 + 5000) / 10000
            modified_color = [
                int(color[0] * strength),
                int(color[1] * strength),
                int(color[2] * strength)
            ]

            self.pixels.setColor(self.addresses[i], modified_color)
        if pixel_breakpoint + 1 < num_pixels:
            for i in range(pixel_breakpoint + 1, num_pixels):
                self.pixels.setColor(self.addresses[i], [0, 0, 0])
