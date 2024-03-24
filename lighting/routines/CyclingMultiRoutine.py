import time

from lighting.routines.Routine import Routine


class CyclingMultiRoutine(Routine):
    duration = 10000
    next_change = 0
    current_routine = None
    current_routine_index = 0
    routines = []

    def __init__(self, routinesWithDuration):
        Routine.__init__(self, None, [])
        self.current_routine = routinesWithDuration[self.current_routine_index][0]
        self.duration = routinesWithDuration[self.current_routine_index][1]
        self.next_change = int(round(time.time() * 1000)) + self.duration
        self.routines = routinesWithDuration

    def tick(self):
        now = int(round(time.time() * 1000))
        if now > self.next_change:
            self.current_routine_index += 1
            self.current_routine_index = self.current_routine_index % len(self.routines)
            self.current_routine = self.routines[self.current_routine_index][0]
            self.duration = self.routines[self.current_routine_index][1]
            self.next_change = now + self.duration
        self.current_routine.tick()