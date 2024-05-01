import RPi.GPIO as GPIO

from lighting.routines import Routines
from ratlantis.Artifact import Artifact
from ratlantis.EnergyVine import EnergyVine
from ratlantis.EnergyTank import EnergyTank
from lighting.PixelControl import PixelControl
from mqtt.MqttClient import MqttClient


class RatGame(object):
    pixels = None
    pixels2 = None
    mqtt = None

    vines = []
    artifacts = []
    tank = None

    is_running = False

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pixels = PixelControl(700, led_brightness=180, led_pin=21)
        self.mqtt = MqttClient()

        vine1 = EnergyVine("2dcc1366080104e0", 4, range(0, 174), self.pixels)
        self.vines.append(vine1)
        vine1.pulse_color()

        # vine2 = EnergyVine("7DC70A09530104E0", 4, range(174, 349), self.pixels)
        # self.vines.append(vine2)
        # vine2.wave()
        #
        # vine3 = EnergyVine("7DC70A09530104E0", 4, range(349, 523), self.pixels)
        # self.vines.append(vine3)
        # vine3.wave()
        #
        # vine4 = EnergyVine("7DC70A09530104E0", 4, range(523, 697), self.pixels)
        # self.vines.append(vine4)
        # vine4.wave()

        artifact = Artifact(self.mqtt, self.pixels, range(697, 698), "noodle/1", self.__on_artifact_change)
        self.artifacts.append(artifact)
        artifact.ring_pulse_color()

        self.tank = EnergyTank(self.mqtt, self.pixels, range(698, 699), range(699, 700), self.__on_artifact_change)
        self.tank.start_charging()

    def __on_artifact_change(self, artifact):
        print("Artifact Changed", artifact)
        for cur_vine in self.vines:
            if cur_vine.rfid == artifact.current_rfid:
                if artifact.current_rfid == artifact.desired_rfid:
                    cur_vine.wave([255, 0, 0])
                    print("Yay connected!")
                else:
                    print("Wrong!!")
                    cur_vine.invalid_connection()
            else:
                cur_vine.pulse_color(1)


    #def start(self):
        #self.vines[0].pulse_color(0)
        #self.artifacts[0].pulse_color(0)

    def update(self):
        for vine in self.vines:
            vine.update()
        for artifact in self.artifacts:
            artifact.update()
        self.tank.update()
        if self.tank.is_full():
            self.tank.start_game()
        self.pixels.render()





