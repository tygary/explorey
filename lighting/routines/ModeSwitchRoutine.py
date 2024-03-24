from lighting.routines.PulseRoutine import PulseRoutine
from lighting.routines.FireRoutine import FireRoutine
from lighting.routines.RainbowRoutine import RainbowRoutine
from lighting.routines.TimeRoutine import TimeRoutine


class ModeSwitchRoutine(TimeRoutine):
    mode = 1
    routines = []

    def __init__(self, pixels, addresses):
        TimeRoutine.__init__(self, pixels, addresses)
        self.routines = [
            PulseRoutine(pixels, [addresses[0]], color=[255, 255, 255]),
            FireRoutine(pixels, [addresses[1]]),
            RainbowRoutine(pixels, [addresses[2]]),
        ]

    def update_mode(self, mode):
        self.mode = mode

    def tick(self):
        for index in range(0, 3):
            if index is not self.mode - 1:
                self.pixels.setColor(self.addresses[index], [0, 0, 0])
        self.routines[self.mode - 1].tick()
