import json

from lighting.PixelDisplay import PixelDisplay
from mqtt.MqttClient import MqttClient


class TimeDisplay(object):
    display = PixelDisplay()
    mqtt = MqttClient()

    def __init__(self):
        self.mqtt.listener(self.__on_event)

    def __on_event(self, event):
        print(f"Got Event: {event}")
        if event:
            data = json.load(event)
            if data:
                self.display.draw_text(data.date)