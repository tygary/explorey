from lighting.routines.Routine import Routine


class BlackoutRoutine(Routine):

    def __init__(self, pixels, addresses, should_override=False):
        super().__init__(self, pixels, addresses, should_override)

    def tick(self):
        for i in self.addresses:
            self.pixels.setColor(i, [0, 0, 0])
