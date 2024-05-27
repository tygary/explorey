import json

from lighting.Colors import Colors
from printer.LeverInputController import LeverInputController
from logger.logger import Logger
from lighting.routines import Routines

ANY_STATE = -1


class Switchboard(object):
    logger = Logger()
    desired_state = [0, 0, 0, 0]
    blackout_addresses = []
    pending_addresses = []
    completed_addresses = []

    def __init__(self, pixels, addresses):
        self.addresses = addresses
        self.pixels = pixels
        self.levers = LeverInputController(self._on_levers_changed, self.logger)
        self.desired_state = self.levers.get_current_values().copy()

        self.blackout_pattern = Routines.BlackoutRoutine(pixels, self.blackout_addresses)
        self.pending_pattern = Routines.RainbowRoutine(pixels, self.pending_addresses)
        self.completed_pattern = Routines.ColorRoutine(pixels, self.completed_addresses, Colors.green)

    def _on_levers_changed(self):
        pass

    def _update_lights(self):
        self.blackout_addresses = []
        self.pending_addresses = []
        self.completed_addresses = []
        for i, address in self.addresses:
            if self.desired_state[i] == ANY_STATE:
                self.blackout_addresses.append(address)
            elif self.desired_state[i] == self.levers.currentValues[i]:
                self.completed_addresses.append(address)
            else:
                self.pending_addresses.append(address)

        self.blackout_pattern.update_addresses(self.blackout_addresses)
        self.completed_pattern.update_addresses(self.completed_addresses)
        self.pending_pattern.update_addresses(self.pending_addresses)

    # def next_desired_state(self, difficulty=1):
        # self.desired_state = []

    def is_completed(self):
        self.levers.get_current_values()
        for i, desired_value in enumerate(self.desired_state):
            if desired_value != self.levers.currentValues[i]:
                return False
        return True

    def update(self):
        self.levers.get_current_values()
        self._update_lights()
        self.blackout_pattern.tick()
        self.pending_pattern.tick()
        self.completed_pattern.tick()





