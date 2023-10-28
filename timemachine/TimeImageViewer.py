import json
from datetime import datetime, timedelta

from mqtt.MqttClient import MqttClient
from timemachine.ImageViewer import ImageViewer

START = datetime(1000, 1, 1, 0, 0, 0)


class TImeImageViewer(object):
    mqtt = MqttClient()
    viewer = ImageViewer()
    date = START
    date_string = ""

    def __init__(self):
        self.mqtt.listen(self.__on_event)

    def __on_event(self, event):
        # print(f"Got Event: {event}")
        # print(self.serial.read())
        if event:
            data = json.loads(event)
            if data["date"]:
                date = START + timedelta(seconds=data["timestamp"])
                self.date = date
                self.date_string = data["date"]
                self.viewer.update(date, data["date"])

