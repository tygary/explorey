from lighting.routines.Routine import Routine


class BlackoutRoutine(Routine):

    def __init__(self, pixels, addresses):
        Routine.__init__(self, pixels, addresses)

    def tick(self):
        for i in self.addresses:
            self.pixels.setColor(i, [0, 0, 0])
