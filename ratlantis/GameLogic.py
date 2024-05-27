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
    switchboard = None

    difficulty = 1
    current_state = STATE_READY

    def __init__(self, vines, artifacts, energy_tank, switchboard):
        self.vines = vines
        self.artifacts = artifacts
        self.energy_tank = energy_tank
        self.switchboard = switchboard

    def _end_game(self):
        print("GAME OVER")
        self.energy_tank.end_game()
        self.start()

    def _get_next_vine(self, excluded_rfid=None):
        vines = []
        for vine in self.vines:
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

        num_to_update = self.difficulty

        artifacts_by_rfid = {}
        for artifact in self.artifacts:
            if artifact.current_rfid is not None:
                artifacts_by_rfid[artifact.current_rfid] = artifact

        artifacts_to_update = random.sample(self.artifacts, num_to_update)
        for artifact in artifacts_to_update:
            vine = self._get_next_vine(excluded_rfid=artifact.current_rfid)
            color = self._get_next_color()
            artifact.set_pending_vine(color, vine.rfid)
            print("artifact ", artifact.id, " is now waiting for ", vine.rfid)

            # If that vine was already connected, then reset the artifact it was connected to
            previous_artifact = artifacts_by_rfid.get(vine.rfid)
            if previous_artifact and previous_artifact != artifact:
                previous_artifact.reset()
                print("artifact", previous_artifact.id, "reset")
        self._update_vine_colors()

        new_switchboard_state = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]
        self.switchboard.desired_state = new_switchboard_state

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




