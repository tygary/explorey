import random
import time
import math
from ratlantis.EnergyVine import COLORS, VINE_ONE_RFID, VINE_TWO_RFID, VINE_THREE_RFID, VINE_FOUR_RFID, VINE_FIVE_RFID, VINE_SIX_RFID, VINE_SEVEN_RFID, VINE_EIGHT_RFID
from ratlantis.Artifact import ARTIFACT_CITY

GAME_MODE_CHARGING = 0
GAME_MODE_READY = 1
GAME_MODE_ROUND_START = 2
GAME_MODE_RUNNING = 3
# GAME_MODE_ENDING = 4
GAME_MODE_WIN = 4
GAME_MODE_LOSE = 5


ARTIFACT_VINE_MATRIX = {
    "artifact/city": [
        VINE_ONE_RFID,
        VINE_TWO_RFID,
        VINE_SEVEN_RFID,
        VINE_EIGHT_RFID
    ],
    "artifact/tank": [
        # VINE_FIVE_RFID,
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
        # VINE_FOUR_RFID
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

ROUND_WAIT_TIME = 10
GAME_OVER_TIME = 10
GAME_WIN_TIME = 55
CHARGING_TIME = 10
LOW_ENERGY_LEVEL_TIME_S = 10


class RoundConfig(object):
    def __init__(self,
                 num_objectives,
                 simultaneous_chance,
                 max_simultaneous,
                 switchboard_rate,
                 drain_time,
                 objective_energy_gain_s,
                 objective_time_length,
                 will_immediately_disconnect):
        self.num_objectives = num_objectives
        self.simultaneous_chance = simultaneous_chance
        self.max_simultaneous = max_simultaneous
        self.switchboard_rate = switchboard_rate
        self.drain_time = drain_time
        self.objective_energy_gain_s = objective_energy_gain_s
        self.objective_time_length = objective_time_length
        self.will_immediately_disconnect = will_immediately_disconnect


ROUND_CONFIG = [
    # 0
    RoundConfig(num_objectives=2,
                simultaneous_chance=0,
                max_simultaneous=1,
                switchboard_rate=0,
                drain_time=30,
                objective_energy_gain_s=20,
                objective_time_length=60,
                will_immediately_disconnect=False),
    # 1
    RoundConfig(num_objectives=4,
                simultaneous_chance=0.25,
                max_simultaneous=2,
                switchboard_rate=0.25,
                drain_time=20,
                objective_energy_gain_s=10,
                objective_time_length=30,
                will_immediately_disconnect=False),
    # 2
    RoundConfig(num_objectives=6,
                simultaneous_chance=0.5,
                max_simultaneous=2,
                switchboard_rate=0.5,
                drain_time=15,
                objective_energy_gain_s=10,
                objective_time_length=20,
                will_immediately_disconnect=False),
    # 3
    RoundConfig(num_objectives=8,
                simultaneous_chance=0.5,
                max_simultaneous=3,
                switchboard_rate=0.75,
                drain_time=10,
                objective_energy_gain_s=10,
                objective_time_length=20,
                will_immediately_disconnect=True),
]


class GameLogic(object):
    vines = []
    artifacts = []
    energy_tank = None
    switchboard = None
    city = None
    mqtt = None

    mode = GAME_MODE_CHARGING
    current_round = 0
    config = ROUND_CONFIG[0]
    remaining_objectives = 0
    next_round_start_time = 0
    celebration_end_time = 0

    last_connected_artifact = None

    def __init__(self, vines, artifacts, energy_tank, switchboard, mqtt, sound, dmx):
        self.vines = vines
        self.artifacts = artifacts
        self.energy_tank = energy_tank
        self.switchboard = switchboard
        self.mqtt = mqtt
        self.sound = sound
        self.dmx = dmx

        for artifact in self.artifacts:
            if artifact.id == ARTIFACT_CITY:
                self.city = artifact
            artifact.reset(allow_any=True)
        self._update_vine_colors()

    def _get_next_vine(self, artifact, excluded_rfids=[]):
        vines = []
        available_vine_ids = ARTIFACT_VINE_MATRIX[artifact.id]
        available_vines = []
        for vine in self.vines:
            if vine.rfid in available_vine_ids:
                available_vines.append(vine)
        for vine in available_vines:
            if vine.rfid not in excluded_rfids:
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
        print("Updating Vine Colors")
        invalid_vines_by_color = {}
        connected_vines_by_color = {}
        pending_vines_by_color = {}
        for artifact in self.artifacts:
            if (artifact.desired_rfid == -1 and artifact.current_rfid) or (artifact.desired_rfid and artifact.desired_rfid == artifact.current_rfid):
                connected_vines_by_color[artifact.current_rfid] = artifact.color
                print(artifact.id, "connected to", artifact.current_rfid)
            elif artifact.current_rfid and artifact.desired_rfid != artifact.current_rfid:
                invalid_vines_by_color[artifact.current_rfid] = artifact.color
                print(artifact.id, "has invalid connection to", artifact.current_rfid)
            elif artifact.desired_rfid and artifact.desired_rfid != -1:
                pending_vines_by_color[artifact.desired_rfid] = artifact.color
                print(artifact.id, artifact.desired_rfid, artifact.color)
        print("invalidVines:", invalid_vines_by_color)
        print("connectedVines:", connected_vines_by_color)
        print("pendingVines:", pending_vines_by_color)
        for vine in self.vines:
            if connected_vines_by_color.get(vine.rfid):
                vine.valid_connection(connected_vines_by_color.get(vine.rfid))
            elif invalid_vines_by_color.get(vine.rfid):
                vine.invalid_connection()
            elif pending_vines_by_color.get(vine.rfid):
                vine.pending_connection(pending_vines_by_color.get(vine.rfid))
            else:
                if self.mode == GAME_MODE_CHARGING or self.mode == GAME_MODE_READY:
                    vine.pending_connection(-1)
                else:
                    vine.off()

    def _update_objectives(self):
        print("Updating Objectives")
        artifacts_by_rfid = {}
        for artifact in self.artifacts:
            if artifact.current_rfid is not None:
                artifacts_by_rfid[artifact.current_rfid] = artifact

        num_to_update = min(random.randint(1, self.config.max_simultaneous), self.remaining_objectives)
        self.remaining_objectives -= num_to_update

        artifacts_without_current = [ artifact for artifact in self.artifacts if artifact != self.last_connected_artifact]
        available_artifacts = self.artifacts if self.config.will_immediately_disconnect else artifacts_without_current
        artifacts_to_update = random.sample(available_artifacts, num_to_update)
        vines_used = []
        for artifact in artifacts_to_update:
            vine = self._get_next_vine(artifact, excluded_rfids=[artifact.current_rfid] + vines_used)
            vines_used.append(vine.rfid)
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
            self.sound.play_pending_switchboard()
        self.mqtt.publish_batch()

    def _change_game_mode(self, new_mode):
        old_mode = self.mode
        self.mode = new_mode
        print("updating game mode from", old_mode, "to", new_mode)
        if new_mode == GAME_MODE_CHARGING:
            print("Game Starting Charging")
            self.sound.play_ambient()
            self.is_charging = True
            self.energy_tank.start_charging()
            self._update_vine_colors()
            self.dmx.change_mode(active=False, startup=False)
        elif new_mode == GAME_MODE_READY:
            print("Game Ready to Start")
            vine = self._get_next_vine(self.energy_tank)
            self.current_round = -1
            self.energy_tank.set_pending_vine(COLORS[3], vine.rfid)
            self._update_vine_colors()
            self.dmx.change_mode(active=False, startup=False)
        elif new_mode == GAME_MODE_ROUND_START:
            self.current_round += 1
            print("Round Starting", self.current_round)
            if self.current_round == 0:
                self.sound.play_game_start()
            else:
                self.sound.play_round_success()
            for artifact in self.artifacts:
                if artifact != self.energy_tank:
                    artifact.reset()
            for vine in self.vines:
                if vine.rfid != self.energy_tank.current_rfid:
                    vine.off()
            self.energy_tank.show_round_num(self.current_round)
            self.config = ROUND_CONFIG[self.current_round]
            self.remaining_objectives = self.config.num_objectives
            self.next_round_start_time = time.time() + ROUND_WAIT_TIME
            print("Now:", time.time(), "Starting round at", self.next_round_start_time)
            self.dmx.change_mode(active=False, startup=True)
        elif new_mode == GAME_MODE_RUNNING:
            print("Go!")
            self.sound.play_running(round_num=self.current_round)
            for artifact in self.artifacts:
                artifact.reset()
            for vine in self.vines:
                vine.off()
            self.mqtt.publish_batch()
            self.energy_tank.start_round(round_time=self.config.objective_time_length)
            self._update_objectives()
            self.dmx.change_mode(active=True, startup=False)
        elif new_mode == GAME_MODE_WIN:
            print("YOU WIN!")
            self.sound.play_you_win()
            self.energy_tank.end_round()
            self.energy_tank.celebrate()
            self.celebration_end_time = time.time() + GAME_WIN_TIME
            self.city.fill_the_city()
            print("Now:", time.time(), "Restarting at", self.celebration_end_time)
            for artifact in self.artifacts:
                artifact.reset()
            self.mqtt.publish_batch()
            for artifact in self.artifacts:
                artifact.reset(allow_any=True)
            self._update_vine_colors()
            self.dmx.change_mode(active=False, startup=True)
        elif new_mode == GAME_MODE_LOSE:
            print("GAME OVER")
            self.sound.play_game_over()
            self.energy_tank.end_round()
            self.energy_tank.mourn()
            for artifact in self.artifacts:
                artifact.reset(allow_any=True)
            self._update_vine_colors()
            self.celebration_end_time = time.time() + GAME_OVER_TIME
            print("Now:", time.time(), "Restarting at", self.celebration_end_time)
            self.dmx.change_mode(active=False, startup=True)

    def artifact_changed(self, artifact, connected, card):
        if connected:
            if artifact.desired_rfid and (artifact.current_rfid == artifact.desired_rfid or artifact.desired_rfid == -1):
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
        for artifact in self.artifacts:
            artifact._send_update()
        self.mqtt.publish_batch()

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
                print("Finished waiting for next round")
                self._change_game_mode(GAME_MODE_RUNNING)
        elif self.mode == GAME_MODE_RUNNING:
            if self.energy_tank.energy_level == 0:
                self._change_game_mode(GAME_MODE_LOSE)
            else:
                if self.energy_tank.energy_level < (100 / self.config.objective_time_length) * LOW_ENERGY_LEVEL_TIME_S:
                    self.sound.play_running_out_of_time()
                else:
                    self.sound.stop_running_out_of_time()
                is_objective_completed = True
                for artifact in self.artifacts:
                    if artifact.current_rfid != artifact.desired_rfid:
                        is_objective_completed = False
                if not self.switchboard.is_completed():
                    is_objective_completed = False
                else:
                    self.sound.stop_pending_switchboard()
                if is_objective_completed:
                    print("Objectives completed")
                    if self.remaining_objectives == 0:
                        print("No objectives left")
                        if self.current_round == len(ROUND_CONFIG) - 1:
                            self._change_game_mode(GAME_MODE_WIN)
                        else:
                            self._change_game_mode(GAME_MODE_ROUND_START)
                    else:
                        gain_in_points = (100 / self.config.objective_time_length) * self.config.objective_energy_gain_s
                        self.energy_tank.add_energy(gain_in_points)
                        self.sound.play_energy_gain()
                        self._update_objectives()
