import json

import numpy

from lighting.PixelDisplay import PixelDisplay
from mqtt.MqttClient import MqttClient
from lighting.UsbSerial import UsbSerial


class TimeDisplay(object):
    display = PixelDisplay()
    mqtt = MqttClient()
    serial = UsbSerial("/dev/ttyACM0")

    def __init__(self):
        self.mqtt.listen(self.__on_event)

    def __on_event(self, event):
        print(f"Got Event: {event}")
        if event:
            data = json.loads(event)
            if data and data["date"]:
                self.display.draw_text(data["date"])
                output = numpy.int16(data['magnitude']).tobytes() + 0x0
                print(output)
                self.serial.write(output)
