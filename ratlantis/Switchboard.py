import random
import time

from lighting.Colors import Colors
from printer.LeverInputController import LeverInputController
from logger.logger import Logger
from lighting.routines import Routines

ANY_STATE = -1

MODE_OFF = 0
MODE_PENDING = 1
MODE_AMBIENT = 2

AMBIENT_CHANGE_TIME_MIN = 3
AMBIENT_CHANGE_TIME_MAX = 20
AMBIENT_COLORS = [
    Colors.green,
    Colors.mixed_blue,
    Colors.light_green,
    Colors.soft_blue,
    Colors.purple,
    Colors.pink,
    Colors.orange,
    Colors.yellow,
]


class Switchboard(object):
    logger = Logger()
    desired_state = [0, 0, 0, 0]
    blackout_addresses = []
    pending_addresses = []
    completed_addresses = []

    top_addresses = []
    bottom_addresses = []

    next_ambient_change_time = time.time()

    mode = MODE_AMBIENT
    ambient_colors_by_addr = {

    }

    def __init__(self, pixels, addresses):
        self.addresses = addresses
        self.top_addresses = [addresses[0], addresses[1], addresses[2], addresses[3]]
        self.bottom_addresses = [addresses[4], addresses[5], addresses[6], addresses[7]]
        self.pixels = pixels
        self.levers = LeverInputController(self._on_levers_changed, self.logger)
        self.desired_state = self.levers.get_current_values().copy()

        self.blackout_pattern = Routines.BlackoutRoutine(pixels, self.blackout_addresses)
        self.pending_pattern = Routines.PulseRoutine(pixels, self.pending_addresses, Colors.red, rate=0.4)
        self.completed_pattern = Routines.ColorRoutine(pixels, self.completed_addresses, Colors.green)
        self.ambient_pattern = Routines.MultiRoutine([
            Routines.ColorRoutine(pixels, [], Colors.green),
            Routines.ColorRoutine(pixels, [], Colors.green),
            Routines.ColorRoutine(pixels, [], Colors.green),
            Routines.ColorRoutine(pixels, [], Colors.green),
        ])

    def _on_levers_changed(self, levers):
        print("Levers Changed", levers)
        pass

    def _update_lights(self):
        if self.mode == MODE_OFF:
            self.blackout_addresses = [self.top_addresses + self.blackout_addresses]
            self.pending_addresses = []
            self.completed_addresses = []
        else:
            if self.mode == MODE_AMBIENT and self.next_ambient_change_time < time.time():
                self.next_ambient_change_time = time.time() + random.randint(AMBIENT_CHANGE_TIME_MIN,
                                                                             AMBIENT_CHANGE_TIME_MAX)
                for i, addr in enumerate(self.top_addresses + self.bottom_addresses):
                    self.ambient_colors_by_addr[addr] = random.choice(AMBIENT_COLORS)
                self.request_new_state(is_ambient=True)

            self.blackout_addresses = []
            self.pending_addresses = []
            self.completed_addresses = []
            for i in range(0, 4):
                # print("checking update", i, self.desired_state, self.levers.currentValues[i])
                if self.desired_state[i] == ANY_STATE:
                    self.blackout_addresses.append(self.top_addresses[i])
                    self.blackout_addresses.append(self.bottom_addresses[i])
                elif self.desired_state[i] == self.levers.currentValues[i]:
                    if self.levers.currentValues[i] == 1:
                        self.completed_addresses.append(self.top_addresses[i])
                        self.blackout_addresses.append(self.bottom_addresses[i])
                    else:
                        self.blackout_addresses.append(self.top_addresses[i])
                        self.completed_addresses.append(self.bottom_addresses[i])
                else:
                    if self.levers.currentValues[i] == 1:
                        self.blackout_addresses.append(self.top_addresses[i])
                        self.pending_addresses.append(self.bottom_addresses[i])
                    else:
                        self.pending_addresses.append(self.top_addresses[i])
                        self.blackout_addresses.append(self.bottom_addresses[i])

        self.blackout_pattern.update_addresses(self.blackout_addresses)
        self.pending_pattern.update_addresses(self.pending_addresses)
        if self.mode == MODE_AMBIENT:
            for i in range(0, 4):
                self.ambient_pattern.routines[i].update_addresses([])
            for i, addr in self.completed_addresses:
                self.ambient_pattern.routines[i].update_addresses([self.completed_addresses[i]])
                self.ambient_pattern.routines[i].update_color(self.ambient_colors_by_addr[addr])
            self.completed_pattern.update_addresses([])
            # print("completed_addresses", [])
            # print("ambient addresses", self.completed_addresses)
        else:
            for i in range(0, 4):
                self.ambient_pattern.routines[i].update_addresses([])
            self.completed_pattern.update_addresses(self.completed_addresses)
            # print("completed_addresses", self.completed_addresses)
            # print("ambient addresses", [])
        # print("blackout addresses", self.blackout_addresses)
        # print("pending_addresses", self.pending_addresses)

    def do_ambient(self):
        self.mode = MODE_AMBIENT
        print("Switchboard - Ambient")

    def clear(self):
        self.mode = MODE_OFF
        print("Switchboard - Clearing")

    def request_new_state(self, is_ambient=False):
        new_switchboard_state = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
        self.desired_state = new_switchboard_state
        print("Switchboard - Getting new State")
        if not is_ambient:
            self.mode = MODE_PENDING
            print("Switchboard - Pending")

    def is_completed(self):
        self.levers.get_current_values()
        for i, desired_value in enumerate(self.desired_state):
            if desired_value != self.levers.currentValues[i]:
                return False
        if self.mode == MODE_PENDING:
            self.mode = MODE_OFF
            print("Switchboard - Done, turning off")
        return True

    def update(self):
        self.levers.get_current_values()
        if self.mode == MODE_PENDING and self.is_completed():
            self.mode = MODE_OFF
            print("Switchboard - Done, turning off")
        self._update_lights()
        self.blackout_pattern.tick()
        self.pending_pattern.tick()
        self.completed_pattern.tick()
        self.ambient_pattern.tick()





