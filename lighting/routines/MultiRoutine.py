from lighting.routines.Routine import Routine


class MultiRoutine(Routine):

    def __init__(self, routines):
        super().__init__(None, [])
        self.routines = routines
        for routine in self.routines:
            print(routine.addresses)

    def tick(self):
        for routine in self.routines:
            routine.tick()
