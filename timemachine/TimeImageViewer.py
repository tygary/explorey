import json
from datetime import datetime, timedelta

from mqtt.MqttClient import MqttClient
from timemachine.ImageViewer import ImageViewer
from timemachine.TimeMachineSoundSystem import TimeMachineSoundSystem

START = datetime(1000, 1, 1, 0, 0, 0)


class TimeImageViewer(object):
    mqtt = MqttClient()
    viewer = ImageViewer()
    music = TimeMachineSoundSystem()
    date = START
    date_string = ""
    magnitude = 0
    data = None

    def __init__(self):
        self.mqtt.listen(self.__on_event)

    def tick(self):
        if self.data:
            self.music.update_sounds(self.data["active"], self.data["magnitude"])

    def __on_event(self, event):
        # print(f"Got Event: {event}")
        # print(self.serial.read())
        if event:
            data = json.loads(event)
            self.data = data
            if data["date"]:
                date = START + timedelta(seconds=data["timestamp"])
                self.date = date
                self.date_string = data["date"]
                self.viewer.update(date, data["date"])

