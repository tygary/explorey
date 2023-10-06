import json

from lighting.PixelDisplay import PixelDisplay
from mqtt.MqttClient import MqttClient


class TimeDisplay(object):
    display = PixelDisplay()
    mqtt = MqttClient()

    def __init__(self):
        self.mqtt.listen(self.__on_event)

    def __on_event(self, event):
        print(f"Got Event: {event}")
        if event:
            data = json.loads(event)
            if data and data["date"]:
                self.display.draw_text(data["date"])
