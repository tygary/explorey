import random
import time
import math
from ratlantis.EnergyVine import COLORS, VINE_ONE_RFID, VINE_TWO_RFID, VINE_THREE_RFID, VINE_FOUR_RFID, VINE_FIVE_RFID, VINE_SIX_RFID, VINE_SEVEN_RFID, VINE_EIGHT_RFID


GAME_MODE_CHARGING = 0
GAME_MODE_READY = 1
GAME_MODE_ROUND_START = 2
GAME_MODE_RUNNING = 3
# GAME_MODE_ENDING = 4
GAME_MODE_WIN = 4
GAME_MODE_LOSE = 5


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
    def __init__(self,
                 num_objectives,
                 simultaneous_chance,
                 max_simultaneous,
                 switchboard_rate,
                 drain_time,
                 objective_energy_gain,
                 objective_time_length,
                 will_immediately_disconnect):
        self.num_objectives = num_objectives
        self.simultaneous_chance = simultaneous_chance
        self.max_simultaneous = max_simultaneous
        self.switchboard_rate = switchboard_rate
        self.drain_time = drain_time
        self.objective_energy_gain = objective_energy_gain
        self.objective_time_length = objective_time_length
        self.will_immediately_disconnect = will_immediately_disconnect


ROUND_CONFIG = [
    # 0
    RoundConfig(num_objectives=2,
                simultaneous_chance=0,
                max_simultaneous=1,
                switchboard_rate=0,
                drain_time=30,
                objective_energy_gain=5,
                objective_time_length=20,
                will_immediately_disconnect=False),
    # 1
    RoundConfig(num_objectives=4,
                simultaneous_chance=0.25,
                max_simultaneous=2,
                switchboard_rate=0.25,
                drain_time=20,
                objective_energy_gain=4,
                objective_time_length=15,
                will_immediately_disconnect=False),
    # 2
    RoundConfig(num_objectives=6,
                simultaneous_chance=0.5,
                max_simultaneous=2,
                switchboard_rate=0.5,
                drain_time=15,
                objective_energy_gain=3,
                objective_time_length=10,
                will_immediately_disconnect=False),
    # 3
    RoundConfig(num_objectives=8,
                simultaneous_chance=0.5,
                max_simultaneous=3,
                switchboard_rate=0.75,
                drain_time=10,
                objective_energy_gain=2,
                objective_time_length=10,
                will_immediately_disconnect=True),
]


class GameLogic(object):
    vines = []
    artifacts = []
    energy_tank = None
    switchboard = None

    mode = GAME_MODE_CHARGING
    current_round = 0
    config = ROUND_CONFIG[0]
    remaining_objectives = 0
    next_round_start_time = 0
    celebration_end_time = 0

    last_connected_artifact = None

    def __init__(self, vines, artifacts, energy_tank, switchboard):
        self.vines = vines
        self.artifacts = artifacts
        self.energy_tank = energy_tank
        self.switchboard = switchboard

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
        invalid_vines_by_color = {}
        connected_vines_by_color = {}
        pending_vines_by_color = {}
        for artifact in self.artifacts:
            if artifact.desired_rfid == -1 or (artifact.desired_rfid and artifact.desired_rfid == artifact.current_rfid):
                connected_vines_by_color[artifact.current_rfid] = artifact.color
                print(artifact.desired_rfid, "connected to", artifact.color)
            elif artifact.current_rfid and artifact.desired_rfid != artifact.current_rfid:
                invalid_vines_by_color[artifact.current_rfid] = artifact.color
                print(artifact.desired_rfid, "has invalid connection to", artifact.color)
            elif artifact.color:
                pending_vines_by_color[artifact.desired_rfid] = artifact.color
                print(artifact.desired_rfid, artifact.color)
        for vine in self.vines:
            if connected_vines_by_color.get(vine.rfid):
                vine.valid_connection(connected_vines_by_color.get(vine.rfid))
            elif invalid_vines_by_color.get(vine.rfid):
                vine.invalid_connection(invalid_vines_by_color.get(vine.rfid))
            elif pending_vines_by_color.get(vine.rfid):
                vine.pending_connection(pending_vines_by_color.get(vine.rfid))
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

        artifacts_without_current = [ artifact for artifact in self.artifacts if artifact != self.last_connected_artifact]
        available_artifacts = self.artifacts if self.config.will_immediately_disconnect else artifacts_without_current
        artifacts_to_update = random.sample(available_artifacts, num_to_update)
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

    def _change_game_mode(self, new_mode):
        old_mode = self.mode
        self.mode = new_mode
        if new_mode == GAME_MODE_CHARGING:
            print("Game Starting Charging")
            self.is_charging = True
            self.energy_tank.start_charging()
            self._update_vine_colors()
        elif new_mode == GAME_MODE_READY:
            print("Game Ready to Start")
            vine = self._get_next_vine(self.energy_tank)
            self.current_round = -1
            self.energy_tank.set_pending_vine(COLORS[3], vine.rfid)
            self._update_vine_colors()
        elif GAME_MODE_ROUND_START:
            print("Round Starting", self.current_round)
            self.energy_tank.end_round()
            self.current_round += 1
            self.energy_tank.show_round_num(self.current_round)
            self.config = ROUND_CONFIG[self.current_round]
            self.remaining_objectives = self.config.num_objectives
            self.next_round_start_time = time.time() + ROUND_WAIT_TIME
            self.is_waiting_for_next_round = True
        elif GAME_MODE_RUNNING:
            print("Go!")
            for artifact in self.artifacts:
                artifact.reset()
            self.energy_tank.start_round(round_time=self.config.objective_time_length)
            self._update_objectives()
        elif GAME_MODE_WIN:
            print("YOU WIN!")
            self.energy_tank.end_round()
            self.energy_tank.celebrate()
            self.celebration_end_time = time.time() + CELEBRATION_TIME
            for artifact in self.artifacts:
                artifact.reset(allow_any=True)
            self._update_vine_colors()
        elif GAME_MODE_LOSE:
            print("GAME OVER")
            self.energy_tank.end_round()
            self.energy_tank.mourn()
            for artifact in self.artifacts:
                artifact.reset(allow_any=True)
            self._update_vine_colors()
            self.celebration_end_time = time.time() + CELEBRATION_TIME

    def artifact_changed(self, artifact, connected, card):
        if connected:
            if artifact.desired_rfid and artifact.current_rfid == artifact.desired_rfid:
                vine = next((vine for vine in self.vines), None)
                # vine.valid_connection(artifact.color)
                print(vine.rfid, "connected to", artifact.id)
                self.last_connected_artifact = artifact
            else:
                print(card, "invalid connection to", artifact.id)
        else:
            self.last_connected_artifact = None
            if artifact.desired_rfid and artifact.desired_rfid == card:
                print(card, "accidentally disconnected from", artifact.id)
            else:
                print(card, "disconnected from", artifact.id)
        self._update_vine_colors()

    def update(self):
        if self.mode == GAME_MODE_LOSE or self.mode == GAME_MODE_WIN:
            if time.time() >= self.celebration_end_time:
                self._change_game_mode(GAME_MODE_CHARGING)
        elif self.mode == GAME_MODE_CHARGING:
            if self.energy_tank.energy_level >= 100:
                self._change_game_mode(GAME_MODE_READY)
        elif self.mode == GAME_MODE_READY:
            if self.energy_tank.desired_rfid == self.energy_tank.current_rfid:
                self._change_game_mode(GAME_MODE_ROUND_START)
        elif self.mode == GAME_MODE_ROUND_START:
            if time.time() >= self.next_round_start_time:
                self._change_game_mode(GAME_MODE_RUNNING)
        elif self.mode == GAME_MODE_RUNNING:
            if self.energy_tank.energy_level == 0:
                self._change_game_mode(GAME_MODE_LOSE)
            else:
                is_objective_completed = True
                for artifact in self.artifacts:
                    if artifact.current_rfid != artifact.desired_rfid:
                        is_objective_completed = False
                if is_objective_completed:
                    if self.remaining_objectives == 0:
                        if self.current_round == len(ROUND_CONFIG) - 1:
                            self._change_game_mode(GAME_MODE_WIN)
                        else:
                            self._change_game_mode(GAME_MODE_ROUND_START)
                    else:
                        self.energy_tank.add_energy(self.config.objective_energy_gain)
                        self._update_objectives()
