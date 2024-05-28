import random
import time
import math
from ratlantis.EnergyVine import COLORS, VINE_ONE_RFID, VINE_TWO_RFID, VINE_THREE_RFID, VINE_FOUR_RFID, VINE_FIVE_RFID, VINE_SIX_RFID, VINE_SEVEN_RFID, VINE_EIGHT_RFID


ARTIFACT_VINE_MATRIX = {
    "artifact/city": [
        VINE_FIVE_RFID,
        VINE_SIX_RFID,
        VINE_SEVEN_RFID,
        VINE_EIGHT_RFID
    ],
    "artifact/tank": [
        VINE_FIVE_RFID,
        VINE_SIX_RFID,
        VINE_SEVEN_RFID,
        VINE_EIGHT_RFID
    ],
    "artifact/mobile": [
        VINE_FIVE_RFID,
        VINE_SIX_RFID,
        VINE_SEVEN_RFID,
        VINE_EIGHT_RFID
    ],
    "artifact/mushrooms": [
        VINE_FIVE_RFID,
        VINE_SIX_RFID,
        VINE_SEVEN_RFID,
        VINE_EIGHT_RFID
    ],
    "artifact/microwave": [
        VINE_ONE_RFID,
        VINE_TWO_RFID,
        VINE_THREE_RFID,
        VINE_FOUR_RFID
    ],
    "artifact/bugs": [
        VINE_ONE_RFID,
        VINE_TWO_RFID,
        VINE_THREE_RFID,
        VINE_FOUR_RFID
    ],
    "artifact/fish": [
        VINE_ONE_RFID,
        VINE_TWO_RFID,
        VINE_THREE_RFID,
        VINE_FOUR_RFID
    ],
    "artifact/volcano": [
        VINE_ONE_RFID,
        VINE_TWO_RFID,
        VINE_THREE_RFID,
        VINE_FOUR_RFID
    ],
}

ROUND_WAIT_TIME = 5
CELEBRATION_TIME = 10
CHARGING_TIME = 20


class RoundConfig(object):
    def __init__(self, num_objectives, simultaneous_chance, max_simultaneous, switchboard_rate, drain_time, objective_energy_gain, objective_time_length):
        self.num_objectives = num_objectives
        self.simultaneous_chance = simultaneous_chance
        self.max_simultaneous = max_simultaneous
        self.switchboard_rate = switchboard_rate
        self.drain_time = drain_time
        self.objective_energy_gain = objective_energy_gain
        self.objective_time_length = objective_time_length


ROUND_CONFIG = [
    RoundConfig(num_objectives=2, simultaneous_chance=0, max_simultaneous=1, switchboard_rate=0, drain_time=30, objective_energy_gain=5, objective_time_length=20),
    RoundConfig(num_objectives=4, simultaneous_chance=0.25, max_simultaneous=2, switchboard_rate=0.25, drain_time=20, objective_energy_gain=4, objective_time_length=15),
    RoundConfig(num_objectives=6, simultaneous_chance=0.5, max_simultaneous=2, switchboard_rate=0.5, drain_time=15, objective_energy_gain=3, objective_time_length=10),
    RoundConfig(num_objectives=8, simultaneous_chance=0.5, max_simultaneous=3, switchboard_rate=0.75, drain_time=10, objective_energy_gain=2, objective_time_length=10),
]


class GameLogic(object):
    vines = []
    artifacts = []
    energy_tank = None
    switchboard = None

    current_round = 0
    config = ROUND_CONFIG[0]
    remaining_objectives = 0
    next_round_start_time = 0
    is_waiting_for_next_round = False
    celebration_end_time = 0
    is_running = False
    is_charging = True
    is_ready_to_start = False


    def __init__(self, vines, artifacts, energy_tank, switchboard):
        self.vines = vines
        self.artifacts = artifacts
        self.energy_tank = energy_tank
        self.switchboard = switchboard

    def _you_win(self):
        print("YOU WIN!")
        self.energy_tank.end_round()
        self.energy_tank.celebrate()
        self.celebration_end_time = time.time() + CELEBRATION_TIME
        self.is_running = False
        self.is_charging = True

    def _end_game(self):
        print("GAME OVER")
        self.energy_tank.end_round()
        self.energy_tank.mourn()
        self.celebration_end_time = time.time() + CELEBRATION_TIME
        self.is_running = False
        self.is_charging = True

    def _get_next_vine(self, artifact, excluded_rfid=""):
        vines = []
        available_vine_ids = ARTIFACT_VINE_MATRIX[artifact.id]
        available_vines = []
        for vine in self.vines:
            if vine.rfid in available_vine_ids:
                available_vines.append(vine)
        for vine in available_vines:
            if vine.rfid != excluded_rfid:
                vines.append(vine)
        return random.choice(vines)

    def _get_next_color(self):
        used_colors = set()
        for artifact in self.artifacts:
            if artifact.color:
                used_colors.add(artifact.color)
        available_colors = [color for color in COLORS if color not in used_colors]
        return random.choice(available_colors)

    def _update_vine_colors(self):
        vines_by_color = {}
        for artifact in self.artifacts:
            if artifact.color:
                vines_by_color[artifact.desired_rfid] = artifact.color
                print(artifact.desired_rfid, artifact.color)
        for vine in self.vines:
            if vines_by_color.get(vine.rfid):
                vine.pending_connection(vines_by_color.get(vine.rfid))
            else:
                vine.off()

    def _update_objectives(self):
        if self.is_waiting_for_next_round:
            if time.time() < self.next_round_start_time:
                return
            else:
                self.is_waiting_for_next_round = False

        artifacts_by_rfid = {}
        for artifact in self.artifacts:
            if artifact.current_rfid is not None:
                artifacts_by_rfid[artifact.current_rfid] = artifact

        num_to_update = min(random.randint(1, self.config.max_simultaneous), self.remaining_objectives)

        artifacts_to_update = random.sample(self.artifacts, num_to_update)
        for artifact in artifacts_to_update:
            vine = self._get_next_vine(artifact, excluded_rfid=artifact.current_rfid)
            color = self._get_next_color()
            artifact.set_pending_vine(color, vine.rfid)
            print("artifact ", artifact.id, " is now waiting for ", vine.rfid)

            # If that vine was already connected, then reset the artifact it was connected to
            previous_artifact = artifacts_by_rfid.get(vine.rfid)
            if previous_artifact and previous_artifact != artifact:
                previous_artifact.reset()
                print("artifact", previous_artifact.id, "reset")
        self._update_vine_colors()

        if random.random() < self.config.switchboard_rate:
            new_switchboard_state = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
            self.switchboard.desired_state = new_switchboard_state

    def next_round(self):
        if self.current_round == len(ROUND_CONFIG) - 1:
            self._you_win()
            return
        self.energy_tank.end_round()
        self.energy_tank.celebrate()
        self.current_round += 1
        self.config = ROUND_CONFIG[0]
        self.remaining_objectives = self.config.num_objectives
        self.next_round_start_time = time.time() + ROUND_WAIT_TIME
        self.is_waiting_for_next_round = True

    def start(self):
        print("Starting game")
        for artifact in self.artifacts:
            artifact.reset()
        self.is_charging = False
        self.is_ready_to_start = False
        self.is_running = True
        self.current_round = -1
        self.next_round()
        self.energy_tank.start_round()
        self._update_objectives()

    def update(self):
        if not self.is_running:
            if time.time() < self.celebration_end_time:
                return
            if not self.is_charging:
                print("Game Starting Charging")
                self.energy_tank.start_charging()
                self._update_vine_colors()
            if self.energy_tank.energy_level == 100 and not self.is_ready_to_start:
                print("Game Ready to Start")
                self.is_ready_to_start = True
                vine = self._get_next_vine(self.energy_tank)
                self.energy_tank.set_pending_vine(COLORS[3], vine.rfid)
                self._update_vine_colors()
            if self.is_ready_to_start:
                if self.energy_tank.desired_rfid == self.energy_tank.current_rfid:
                    self.start()
        else:
            if self.energy_tank.energy_level == 0:
                self._end_game()
                return

            is_objective_completed = True
            for artifact in self.artifacts:
                if artifact.current_rfid != artifact.desired_rfid:
                    is_objective_completed = False

            if is_objective_completed:
                if self.remaining_objectives == 0:
                    self.next_round()
                self._update_objectives()
                if not self.is_waiting_for_next_round:
                    self.energy_tank.add_energy(self.config.objective_energy_gain)




