from lighting.routines.Routine import Routine


class ColorRoutine(Routine):

    def __init__(self, pixels, addresses, color, should_override=False, brightness=1.0):
        super().__init__(pixels, addresses, should_override, brightness)
        self.color = color

    def update_color(self, color):
        self.color = color

    def tick(self):
        for i in self.addresses:
            self.pixels.setColor(i, self.color)
