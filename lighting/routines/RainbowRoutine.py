from lighting.routines.Routine import Routine


class RainbowRoutine(Routine):
    values = {}

    def __init__(self, pixels, addresses):
        Routine.__init__(self, pixels, addresses)
        for i in self.addresses:
            red = 100 + i % 255
            green = i % 255
            blue = 200 + i % 255
            self.values[i] = [red, green, blue]

    def update_addresses(self, addresses):
        if set(addresses) != set(self.addresses):
            super().update_addresses(addresses)
            self.values = {}
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
