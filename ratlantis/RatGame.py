from ratlantis.Artifact import Artifact
from ratlantis.EnergyVine import EnergyVine
from lighting.PixelControl import PixelControl
from mqtt.MqttClient import MqttClient


class RatGame(object):
    pixels = None
    mqtt = None

    vines: = []
    artifacts: = []

    is_running = False

    def __init__(self):
        self.pixels = PixelControl(100)
        self.mqtt = MqttClient()

        vine = EnergyVine("noodle1", 10, range(0, 50), self.pixels)
        self.vines.append(vine)

        artifact = Artifact(self.mqtt, self.pixels, range(51, 60), "noodle1", self.__on_artifact_change)
        self.artifacts.append(artifact)

    def __on_artifact_change(self, artifact: Artifact):
        print("Artifact Changed", artifact)
        vine = None
        for cur_vine in self.vines:
            if cur_vine.rfid == artifact.current_rfid:
                vine = cur_vine

        if vine:
            vine.detach()
            # artifact.wave([255, 0, 0])
            # artifact.is_activated = True
            # vine.wave([255, 0, 0])
        #else:
            # artifact.pulse_color(0)
            # vine.pulse_color(0)
            # artifact.is_activated = False

    #def start(self):
        #self.vines[0].pulse_color(0)
        #self.artifacts[0].pulse_color(0)

    def update(self):
        for vine in self.vines:
            vine.update()
        for artifact in self.artifacts:
            artifact.update()





