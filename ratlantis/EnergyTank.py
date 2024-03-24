import math
import time

from lighting.routines.Routine import Routines
from lighting.Colors import Colors
from ratlantis.Artifact import Artifact

CARD_FOUND = "cardFound"
CARD_REMOVED = "cardRemoved"

GAME_LENGTH_S = 60
MAX_ENERGY = 100
ENERGY_LEVEL_TRANSITION_RATE_PER_SEC = 10
DRAIN_RATE = MAX_ENERGY / GAME_LENGTH_S

NEARLY_EMPTY_THRESHOLD = 10

MODE_OFF = 0
MODE_OFF_CHARGING = 1
MODE_FULL = 2
MODE_RUNNING = 3
MODE_NEARLY_EMPTY = 4

TANK_ID = "tank"

TANK_COLOR = Colors.green
TANK_COLORS = [TANK_COLOR, Colors.light_green, Colors.mid_green]


class EnergyTank(Artifact):
    energy_level = 0
    rendered_energy_level = 0

    last_update = 0
    outer_callback = None
    is_active = False
    is_charging = False
    mode = MODE_OFF

    tank_light_addresses = []
    tank_routine = None

    def __init__(self, mqtt, pixels, ring_light_addresses, tank_light_addresses, on_change):
        self.outer_callback = on_change
        self.tank_light_addresses = tank_light_addresses
        Artifact.__init__(self, mqtt, pixels, ring_light_addresses, TANK_ID, self.__on_artifact_change)
        self.last_update = time.time()
        self.__update_light_routing()

    # ---------------------------------------

    def __on_artifact_change(self):
        # Can intercept change event here
        self.outer_callback(self)

    def __update_rendered_energy(self, time_since_last_update):
        direction = 1
        if self.rendered_energy_level > self.energy_level:
            direction = -1
        change = min(
            abs(self.rendered_energy_level - self.energy_level),
            time_since_last_update * ENERGY_LEVEL_TRANSITION_RATE_PER_SEC
        )
        self.rendered_energy_level = self.rendered_energy_level + (direction * change)

    def __get_new_mode(self):
        if self.rendered_energy_level == 0:
            return MODE_OFF
        if self.mode == MODE_OFF_CHARGING and self.rendered_energy_level == MAX_ENERGY:
            self.is_charging = False
            return MODE_FULL
        if self.is_charging:
            return MODE_OFF_CHARGING
        if self.rendered_energy_level <= NEARLY_EMPTY_THRESHOLD:
            return MODE_NEARLY_EMPTY
        if self.is_active:
            return MODE_RUNNING

    def __get_powered_light_addresses(self):
        energy_ratio = self.rendered_energy_level / MAX_ENERGY
        highest_index = math.floor(energy_ratio * (len(self.tank_light_addresses)))
        active_pixels = self.tank_light_addresses[0:highest_index]
        inactive_pixels = self.tank_light_addresses[highest_index:len(self.tank_light_addresses)]
        return active_pixels, inactive_pixels

    def __update_light_routing(self):
        active_pixels, inactive_pixels = self.__get_powered_light_addresses()
        if self.mode == MODE_OFF:
            self.tank_routine = Routines.MultiRoutine([
                Routines.BlackoutRoutine(self.pixels, self.tank_light_addresses)
            ])
        elif self.mode == MODE_OFF_CHARGING:
            self.tank_routine = Routines.MultiRoutine([
                Routines.WaveRoutine(self.pixels, active_pixels, TANK_COLORS),
                Routines.BlackoutRoutine(self.pixels, inactive_pixels)
            ])
        elif self.mode == MODE_FULL:
            self.tank_routine = Routines.MultiRoutine([
                Routines.FireRoutine(self.pixels, self.tank_light_addresses, TANK_COLORS)
            ])
        elif self.mode == MODE_RUNNING:
            self.tank_routine = Routines.MultiRoutine([
                Routines.FireRoutine(self.pixels, active_pixels),
                Routines.BlackoutRoutine(self.pixels, inactive_pixels)
            ])
        elif self.mode == MODE_NEARLY_EMPTY:
            self.tank_routine = Routines.MultiRoutine([
                Routines.PulseRoutine(self.pixels, active_pixels, TANK_COLOR),
                Routines.BlackoutRoutine(self.pixels, inactive_pixels)
            ])

    # ---------------------------------------

    def start_charging(self):
        self.is_active = False
        self.is_charging = True
        self.energy_level = 1
        self.rendered_energy_level = 1

    def is_full(self):
        return self.mode == MODE_FULL

    def start_game(self):
        self.last_update = time.time()
        self.energy_level = MAX_ENERGY
        self.rendered_energy_level = MAX_ENERGY
        self.is_active = True
        self.is_charging = False

    def end_game(self):
        self.energy_level = 0
        self.rendered_energy_level = 0
        self.is_active = False
        self.is_charging = False

    def add_energy(self, amount):
        self.energy_level += amount
        if self.energy_level < 0:
            self.energy_level = 0
        elif self.energy_level > MAX_ENERGY:
            self.energy_level = MAX_ENERGY

    def update(self):
        now = time.time()
        time_since_last_update = now - self.last_update
        if time_since_last_update > 0:
            prev_active_addresses, prev_inactive_addresses = self.__get_powered_light_addresses()
            if self.is_active:
                self.energy_level = self.energy_level - (time_since_last_update * DRAIN_RATE)
            self.__update_rendered_energy(time_since_last_update)
            active_addresses, inactive_addresses = self.__get_powered_light_addresses()
            if self.tank_routine.routines and (prev_active_addresses is not active_addresses):
                if len(self.tank_routine.routines) == 2:
                    self.tank_routine.routines[0].update_addresses(active_addresses)
                    self.tank_routine.routines[1].update_addresses(inactive_addresses)
        new_mode = self.__get_new_mode()
        if new_mode != self.mode:
            self.mode = new_mode
            self.__update_light_routing()
        Artifact.update(self)
        self.last_update = now



