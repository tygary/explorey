import RPi.GPIO as GPIO

from ratlantis.Artifact import Artifact
from ratlantis.EnergyVine import EnergyVine
from lighting.PixelControl import PixelControl
from mqtt.MqttClient import MqttClient


class RatGame(object):
    pixels = None
    mqtt = None

    vines = []
    artifacts = []

    is_running = False

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pixels = PixelControl(1000)
        self.mqtt = MqttClient()

        vine = EnergyVine("7DC70A09530104E0", 4, range(0, 1000), self.pixels)
        self.vines.append(vine)

        artifact = Artifact(self.mqtt, self.pixels, range(51, 60), "noodle1", self.__on_artifact_change)
        self.artifacts.append(artifact)

    def __on_artifact_change(self, artifact):
        print("Artifact Changed", artifact)
        vine = None
        for cur_vine in self.vines:
            if cur_vine.rfid == artifact.current_rfid:
                vine = cur_vine
        print(vine)
        if vine:
            vine.detach()
            # artifact.wave([255, 0, 0])
            # artifact.is_activated = True
            vine.wave([255, 0, 0])
        else:
            # artifact.pulse_color(0)
            vine.pulse_color(0)
            # artifact.is_activated = False

    #def start(self):
        #self.vines[0].pulse_color(0)
        #self.artifacts[0].pulse_color(0)

    def update(self):
        for vine in self.vines:
            vine.update()
        for artifact in self.artifacts:
            artifact.update()





