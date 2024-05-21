import RPi.GPIO as GPIO
import random

from lighting.routines import Routines
from ratlantis.Artifact import Artifact
from ratlantis.EnergyVine import *
from ratlantis.EnergyTank import EnergyTank
from ratlantis.GameLogic import GameLogic
from lighting.PixelControl import PixelControl
from mqtt.MqttClient import MqttClient

TEST_RFID = "2dcc1366080104e0"


class RatGame(object):
    pixels = None
    pixels2 = None
    mqtt = None
    current_color = COLOR_BLUE

    game = None
    vines = []
    artifacts = []
    tank = None

    is_running = False

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pixels = PixelControl(700, led_brightness=180, led_pin=21)
        self.mqtt = MqttClient()

        vine1 = EnergyVine("2dcc1366080104e0", range(0, 174), self.pixels)
        self.vines.append(vine1)
        vine1.pending_connection(self.current_color)

        vine2 = EnergyVine("f1011466080104e0", range(174, 349), self.pixels)
        self.vines.append(vine2)
        vine2.pending_connection(self.current_color)
        #
        # vine3 = EnergyVine("7DC70A09530104E0", range(349, 523), self.pixels)
        # self.vines.append(vine3)
        # vine3.pending_connection(self.current_color)
        #
        # vine4 = EnergyVine("7DC70A09530104E0", range(523, 697), self.pixels)
        # self.vines.append(vine4)
        # vine4.pending_connection(self.current_color)
        #
        artifact = Artifact(self.mqtt, "noodle/1", self.__on_artifact_change)
        self.artifacts.append(artifact)

        artifact = Artifact(self.mqtt, "noodle/9", self.__on_artifact_change)
        self.artifacts.append(artifact)
        #
        self.tank = EnergyTank(self.mqtt, self.pixels, range(698, 699), self.__on_artifact_change)
        self.tank.start_charging()

        self.game = GameLogic(self.vines, self.artifacts, self.tank, None)
        self.game.start()

    def __on_artifact_change(self, artifact):
        print("Artifact Changed", artifact)
        cur_vine = self.vines[0]
        if artifact.current_rfid:
            if artifact.current_rfid == artifact.desired_rfid:
                cur_vine.valid_connection(self.current_color)
                print("Yay connected!")
            else:
                print("Wrong!!")
                cur_vine.invalid_connection()
        # else:
            # self.current_color = random.choice(COLORS)
            # artifact.set_pending_vine(self.current_color, TEST_RFID)
            # cur_vine.pending_connection(self.current_color)


    #def start(self):
        #self.vines[0].pulse_color(0)
        #self.artifacts[0].pulse_color(0)

    def update(self):
        self.game.update()
        for vine in self.vines:
            vine.update()
        # self.tank.update()
        # if self.tank.is_full():
        #     self.tank.start_game()
        self.pixels.render()





