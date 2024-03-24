import time

from lighting.routines.Routine import Routine


class TimeRoutine(Routine):
    now = 0

    def __init__(self, pixels, addresses):
        Routine.__init__(self, pixels, addresses)
        self.update_now()

    def tick(self):
        self.update_now()

    def update_now(self):
        self.now = int(round(time.time() * 1000))
