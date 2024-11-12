from lighting.routines.PulseRoutine import PulseRoutine
from lighting.routines.RainbowRoutine import RainbowRoutine
from lighting.routines.TimeRoutine import TimeRoutine


class ModeRoutine(TimeRoutine):
    mode = 1
    routines = []

    def __init__(self, pixels, addresses):
        super().__init__(self, pixels, addresses)
        self.routines = [
            PulseRoutine(pixels, [addresses[0]], color=[255, 255, 255]),
            PulseRoutine(pixels, [addresses[1]], color=[255, 0, 0]),
            PulseRoutine(pixels, [addresses[2]], color=[0, 255, 0]),
            PulseRoutine(pixels, [addresses[3]], color=[0, 0, 255]),
            PulseRoutine(pixels, [addresses[4]], color=[255, 255, 0]),
            PulseRoutine(pixels, [addresses[5]], color=[0, 255, 255]),
            PulseRoutine(pixels, [addresses[6]], color=[255, 0, 255]),
            RainbowRoutine(pixels, [addresses[7]]),
        ]

    def update_mode(self, mode):
        self.mode = mode

    def tick(self):
        for index in range(0, 8):
            if index is not self.mode - 1:
                self.pixels.setColor(self.addresses[index], [0, 0, 0])
        self.routines[self.mode - 1].tick()
