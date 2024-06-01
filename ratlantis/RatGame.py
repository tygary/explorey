import RPi.GPIO as GPIO
import random

from lighting.routines import Routines
from ratlantis.Artifact import *
from ratlantis.EnergyVine import *
from ratlantis.EnergyTank import EnergyTank
from ratlantis.GameLogic import GameLogic
from ratlantis.Switchboard import Switchboard
from ratlantis.RatGameSoundSystem import RatGameSoundSystem
from ratlantis.RatDmx import RatDmx
from lighting.PixelControl import PixelControl
from mqtt.MqttClient import MqttClient

TEST_RFID = "2dcc1366080104e0"


class RatGame(object):
    pixels = None
    pixels2 = None
    mqtt = None
    current_color = COLOR_BLUE
    dmx = RatDmx()

    game = None
    vines = []
    artifacts = []
    tank = None
    switchboard = None

    is_running = False

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pixels = PixelControl(150, led_brightness=200, led_pin=21)
        self.mqtt = MqttClient()
        self.sound = RatGameSoundSystem()

        # self.vines.append(RemoteEnergyVine(VINE_ONE_RFID, self.mqtt))
        # self.vines.append(RemoteEnergyVine(VINE_TWO_RFID, self.mqtt))
        # self.vines.append(RemoteEnergyVine(VINE_THREE_RFID, self.mqtt))
        # self.vines.append(RemoteEnergyVine(VINE_FOUR_RFID, self.mqtt))
        self.vines.append(RemoteEnergyVine(VINE_FIVE_RFID, self.mqtt))
        self.vines.append(RemoteEnergyVine(VINE_SIX_RFID, self.mqtt))
        self.vines.append(RemoteEnergyVine(VINE_SEVEN_RFID, self.mqtt))
        self.vines.append(RemoteEnergyVine(VINE_EIGHT_RFID, self.mqtt))

        self.artifacts.append(Artifact(self.mqtt, ARTIFACT_CITY, self.__on_artifact_change))
        self.artifacts.append(Artifact(self.mqtt, ARTIFACT_MOBILE, self.__on_artifact_change))
        self.artifacts.append(Artifact(self.mqtt, ARTIFACT_MUSHROOMS, self.__on_artifact_change))
        #
        # self.artifacts.append(Artifact(self.mqtt, ARTIFACT_BUGS, self.__on_artifact_change))
        # self.artifacts.append(Artifact(self.mqtt, ARTIFACT_VOLCANO, self.__on_artifact_change))
        # self.artifacts.append(Artifact(self.mqtt, ARTIFACT_FISH, self.__on_artifact_change))
        # self.artifacts.append(Artifact(self.mqtt, ARTIFACT_MICROWAVE, self.__on_artifact_change))

        self.tank = EnergyTank(self.mqtt, self.pixels, range(54, 150), self.__on_artifact_change)
        self.artifacts.append(self.tank)
        self.tank.start_charging()

        self.switchboard = Switchboard(self.pixels, [4, 3, 2, 1, 8, 9, 10, 11])

        self.game = GameLogic(self.vines, self.artifacts, self.tank, self.switchboard, self.mqtt, self.sound, self.dmx)

    def __on_artifact_change(self, artifact, connected, card):
        print("Artifact Changed", artifact)
        self.game.artifact_changed(artifact, connected, card)
        # cur_vine = self.vines[0]
        # if artifact.current_rfid:
        #     if artifact.current_rfid == artifact.desired_rfid:
        #         cur_vine.valid_connection(self.current_color)
        #
        #         print("Yay connected!")
        #     else:
        #         print("Wrong!!")
        #         cur_vine.invalid_connection()
        # else:
            # self.current_color = random.choice(COLORS)
            # artifact.set_pending_vine(self.current_color, TEST_RFID)
            # cur_vine.pending_connection(self.current_color)

    def update(self):
        self.game.update()
        self.tank.update()
        self.mqtt.publish_batch()
        self.switchboard.update()
        self.pixels.render()
        self.dmx.update()






