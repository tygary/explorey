from lighting.routines.Routine import Routine


class ColorRoutine(Routine):

    def __init__(self, pixels, addresses, color):
        self.color = color
        Routine.__init__(self, pixels, addresses)

    def tick(self):
        for i in self.addresses:
            self.pixels.setColor(i, self.color)
