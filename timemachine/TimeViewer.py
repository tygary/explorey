import json
import datetime

from mqtt.MqttClient import MqttClient
from timemachine.ImageViewer import ImageViewer


class TimeViewer(object):
    mqtt = MqttClient()
    viewer = ImageViewer()

    def __init__(self):
        self.mqtt.listen(self.__on_event)

    def __on_event(self, event):
        print(f"Got Event: {event}")
        print(self.serial.read())
        if event:
            data = json.loads(event)
            if data["date"]:
                self.viewer.update(datetime.datetime(1970, 1, 1), data["date"])
