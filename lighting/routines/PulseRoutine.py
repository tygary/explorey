from lighting.routines.Routine import Routine


class PulseRoutine(Routine):
    going_up = True
    color = None
    ratio = 0
    values = []
    rate = 0.05

    def __init__(self, pixels, addresses, color, rate=0.05):
        Routine.__init__(self, pixels, addresses)
        self.color = color
        self.rate = rate
        for i, address in enumerate(self.addresses):
            red = 0
            green = 0
            blue = 0
            self.values.append([red, green, blue])

    def update_addresses(self, addresses):
        Routine.update_addresses(self, addresses)
        old_values = self.values
        self.values = []
        last_value = [0, 0, 0]
        for i, address in enumerate(addresses):
            if i < len(old_values):
                self.values.append(old_values[i])
                last_value = self.values[i]
            else:
                self.values.append([
                    last_value[0],
                    last_value[1],
                    last_value[2],
                ])

    def tick(self):
        if self.ratio >= 1:
            self.going_up = False
        if self.ratio <= 0:
            self.going_up = True
        if self.going_up:
            self.ratio += self.rate
            if self.ratio > 1:
                self.ratio = 1
        else:
            self.ratio -= self.rate
            if self.ratio < 0:
                self.ratio = 0

        for i, address in enumerate(self.addresses):
            self.values[i][0] = int(self.ratio * self.color[0])
            self.values[i][1] = int(self.ratio * self.color[1])
            self.values[i][2] = int(self.ratio * self.color[2])
            self.pixels.setColor(address, self.values[i])
