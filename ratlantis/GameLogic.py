import random
from ratlantis.EnergyVine import COLORS


STATE_READY = 0
STATE_RUNNING = 1
STATE_FAILURE = 2
STATE_SUCCESS = 3


ENERGY_GAIN_PER_OBJECTIVE = 30

class GameLogic(object):
    vines = []
    artifacts = []
    energy_tank = None
    levers = None

    difficulty = 1
    current_state = STATE_READY

    def __init__(self, vines, artifacts, energy_tank, levers):
        self.vines = vines
        self.artifacts = artifacts
        self.energy_tank = energy_tank
        self.levers = levers

    def _end_game(self):
        print("GAME OVER")
        self.energy_tank.end_game()

    def _get_next_vine(self, exclusion=None):
        vines = []
        for vine in self.vines:
            if vine.rfid != exclusion:
                vines.append(vine)
        return random.choice(vines)

    def _get_next_color(self, exclusion=None):
        used_colors = set()
        for artifact in self.artifacts:
            if artifact.color and artifact != exclusion:
                used_colors.add(artifact.color)
        available_colors = [color for color in COLORS if color not in used_colors]
        return random.choice(available_colors)

    def _update_objectives(self):

        num_to_update = self.difficulty

        artifacts_to_update = random.sample(self.artifacts, num_to_update)
        for artifact in artifacts_to_update:
            vine = self._get_next_vine(exclusion=artifact.current_rfid)
            color = self._get_next_color(exclusion=artifact)
            artifact.set_pending_vine(color, vine.rfid)

    def start(self):
        print("Starting game")
        self.energy_tank.start_game()
        self._update_objectives()

    def update(self):
        if self.energy_tank.energy_level == 0:
            self._end_game()
            return

        is_objective_completed = True
        for artifact in self.artifacts:
            if artifact.current_rfid != artifact.desired_rfid:
                is_objective_completed = False

        if is_objective_completed:
            self._update_objectives()
            self.energy_tank.add_energy(ENERGY_GAIN_PER_OBJECTIVE)




