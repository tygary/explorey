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
        self.pixels = PixelControl(300, led_brightness=250, led_pin=21)
        self.mqtt = MqttClient()

        vine = EnergyVine("7DC70A09530104E0", 4, range(0, 160), self.pixels)
        self.vines.append(vine)
        vine.pulse_color(0)

        artifact = Artifact(self.mqtt, self.pixels, range(161, 162), "noodle1", self.__on_artifact_change)
        self.artifacts.append(artifact)
        artifact.ring_pulse_color()

        self.tank = EnergyTank(self.mqtt, self.pixels, range(162, 163), range(163, 300), self.__on_artifact_change)
        self.tank.start_charging()

    def __on_artifact_change(self, artifact):
        print("Artifact Changed", artifact)
        for cur_vine in self.vines:
            if cur_vine.rfid == artifact.current_rfid:
                print(cur_vine)
                cur_vine.detach()
                cur_vine.wave([255, 0, 0])
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





