import math
import time

from ratlantis.Artifact import *

CARD_FOUND = "cardFound"
CARD_REMOVED = "cardRemoved"

GAME_LENGTH_S = 60
CHARGING_TIME_S = 20
MAX_ENERGY = 100
# DRAIN_RATE = MAX_ENERGY / GAME_LENGTH_S
CHARGE_RATE = MAX_ENERGY / CHARGING_TIME_S
ENERGY_LEVEL_TRANSITION_RATE_PER_SEC = CHARGE_RATE

NEARLY_EMPTY_THRESHOLD = 10

MODE_OFF = 0
MODE_OFF_CHARGING = 1
MODE_FULL = 2
MODE_RUNNING = 3
MODE_NEARLY_EMPTY = 4
MODE_CELEBRATE = 5
MODE_MOURN = 6
MODE_ROUND_START = 7

TANK_COLOR = Colors.green
TANK_COLORS = [TANK_COLOR, Colors.light_green, Colors.mid_green]


class EnergyTank(Artifact):
    energy_level = 0
    rendered_energy_level = 0

    drain_rate = 0

    last_update = 0
    outer_callback = None
    is_active = False
    is_charging = False
    mode = MODE_OFF
    round_num = 0

    tank_light_addresses = []
    segment_addresses = [
        range(0, 33),
        range(33, 66),
        range(66, 100)
    ]

    tank_routine = None

    def __init__(self, mqtt, pixels, tank_light_addresses, on_change):
        self.outer_callback = on_change
        self.pixels = pixels
        self.tank_light_addresses = tank_light_addresses
        Artifact.__init__(self, mqtt, ARTIFACT_TANK, self.__on_artifact_change)
        self.last_update = time.time()
        self.__update_light_routing()

    # ---------------------------------------

    def __on_artifact_change(self, artifact, connected, card):
        # Can intercept change event here
        self.outer_callback(artifact, connected, card)

    def __update_rendered_energy(self, time_since_last_update):
        direction = 1
        if self.rendered_energy_level > self.energy_level:
            direction = -1
        change = min(
            abs(self.rendered_energy_level - self.energy_level),
            time_since_last_update * ENERGY_LEVEL_TRANSITION_RATE_PER_SEC
        )
        # self.rendered_energy_level = self.rendered_energy_level + (direction * change)
        # Temp hack to keep it simple...
        self.rendered_energy_level = self.energy_level

    def __get_new_mode(self):
        if self.mode == MODE_CELEBRATE or self.mode == MODE_MOURN or self.mode == MODE_ROUND_START:
            return self.mode
        if self.rendered_energy_level <= 0:
            self.energy_level = 0
            self.rendered_energy_level = 0
            self.is_active = False
            return MODE_OFF
        if self.mode == MODE_OFF_CHARGING and self.rendered_energy_level >= MAX_ENERGY:
            self.energy_level = MAX_ENERGY
            self.rendered_energy_level = MAX_ENERGY
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
        highest_index = math.floor(energy_ratio * (len(self.tank_light_addresses) - 1))
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
                Routines.PulseRoutine(self.pixels, active_pixels, Colors.light_green),
                Routines.BlackoutRoutine(self.pixels, inactive_pixels)
            ])
        elif self.mode == MODE_FULL:
            self.tank_routine = Routines.MultiRoutine([
                Routines.FireRoutine(self.pixels, self.tank_light_addresses, TANK_COLORS)
            ])
        elif self.mode == MODE_RUNNING:
            self.tank_routine = Routines.MultiRoutine([
                Routines.FireRoutine(self.pixels, active_pixels, TANK_COLORS),
                Routines.BlackoutRoutine(self.pixels, inactive_pixels)
            ])
        elif self.mode == MODE_NEARLY_EMPTY:
            self.tank_routine = Routines.MultiRoutine([
                Routines.PulseRoutine(self.pixels, active_pixels, TANK_COLOR),
                Routines.BlackoutRoutine(self.pixels, inactive_pixels)
            ])
        elif self.mode == MODE_CELEBRATE:
            self.tank_routine = Routines.MultiRoutine([
                Routines.RainbowRoutine(self.pixels, self.tank_light_addresses)
            ])
        elif self.mode == MODE_MOURN:
            self.tank_routine = Routines.MultiRoutine([
                Routines.FireRoutine(self.pixels, self.tank_light_addresses, Colors.red)
            ])
        elif self.mode == MODE_ROUND_START:
            if self.round_num == 3:
                self.tank_routine = Routines.MultiRoutine([
                    Routines.PulseRoutine(self.pixels, self.tank_light_addresses, Colors.mixed_blue),
                ])
            else:
                lit_addresses = []
                blackout_addresses = []
                for i in range(0, 3):
                    if i <= self.round_num:
                        for addr_index in self.segment_addresses[i]:
                            lit_addresses.append(self.tank_light_addresses[addr_index])
                    else:
                        for addr_index in self.segment_addresses[i]:
                            blackout_addresses.append(self.tank_light_addresses[addr_index])
                self.tank_routine = Routines.MultiRoutine([
                    Routines.PulseRoutine(self.pixels, lit_addresses, Colors.green),
                    Routines.BlackoutRoutine(self.pixels, blackout_addresses)
                ])

    # ---------------------------------------

    def start_charging(self):
        print("Tank starting charging")
        self.mode = -1
        self.is_active = False
        self.is_charging = True
        self.energy_level = 1
        self.rendered_energy_level = 1
        self.last_update = time.time()

    def is_full(self):
        return self.mode == MODE_FULL

    def start_round(self, round_time=GAME_LENGTH_S):
        print("Tank starting round", round_time)
        self.mode = MODE_RUNNING
        self.last_update = time.time()
        self.energy_level = MAX_ENERGY
        self.rendered_energy_level = MAX_ENERGY
        self.drain_rate = MAX_ENERGY / round_time
        self.is_active = True
        self.is_charging = False
        self.__update_light_routing()

    def celebrate(self):
        print("Tank is Celebrating")
        self.mode = MODE_CELEBRATE
        self.energy_level = 0
        self.is_active = False
        self.is_charging = False
        self.last_update = time.time()
        self.__update_light_routing()

    def mourn(self):
        print("Tank is Mourning")
        self.mode = MODE_MOURN
        self.energy_level = 0
        self.is_active = False
        self.is_charging = False
        self.last_update = time.time()
        self.__update_light_routing()

    def show_round_num(self, round_num):
        print("Tank Showing Round Num", round_num)
        self.mode = MODE_ROUND_START
        self.round_num = round_num
        self.energy_level = MAX_ENERGY
        self.is_active = False
        self.is_charging = False
        self.last_update = time.time()
        self.__update_light_routing()
        # TODO display number in lights

    def end_round(self):
        print("Tank round ended")
        self.mode = -1
        self.energy_level = 0
        self.rendered_energy_level = 0
        self.is_active = False
        self.is_charging = False
        self.last_update = time.time()
        self.__update_light_routing()

    def add_energy(self, amount):
        self.energy_level += amount
        if self.energy_level < 0:
            self.energy_level = 0
        elif self.energy_level > MAX_ENERGY:
            self.energy_level = MAX_ENERGY
        print("Tank Gained energy", amount, "to be", self.energy_level)

    def update(self):
        now = time.time()
        time_since_last_update = now - self.last_update
        if time_since_last_update > 0 and (self.is_charging or self.is_active):
            prev_active_addresses, prev_inactive_addresses = self.__get_powered_light_addresses()
            if self.is_active:
                # print("Drained power by ", time_since_last_update * self.drain_rate)
                self.energy_level = self.energy_level - (time_since_last_update * self.drain_rate)
            elif self.is_charging:
                self.energy_level = self.energy_level + (time_since_last_update * CHARGE_RATE)
            self.__update_rendered_energy(time_since_last_update)
            active_addresses, inactive_addresses = self.__get_powered_light_addresses()
            if self.tank_routine.routines and len(prev_active_addresses) != len(active_addresses):
                if len(self.tank_routine.routines) == 2:
                    self.tank_routine.routines[0].update_addresses(active_addresses)
                    self.tank_routine.routines[1].update_addresses(inactive_addresses)
        new_mode = self.__get_new_mode()
        if new_mode != self.mode:
            print("Updating energy tank mode to ", new_mode)
            self.mode = new_mode
            self.__update_light_routing()
        self.tank_routine.tick()
        self.last_update = now



