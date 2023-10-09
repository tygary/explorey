import json

import numpy

from lighting.PixelDisplay import PixelDisplay
from mqtt.MqttClient import MqttClient
from lighting.UsbSerial import UsbSerial


class TimeDisplay(object):
    display = PixelDisplay()
    mqtt = MqttClient()
    serial = UsbSerial("/dev/ttyUSB1")

    def __init__(self):
        self.mqtt.listen(self.__on_event)

    def __on_event(self, event):
        print(f"Got Event: {event}")
        if event:
            data = json.loads(event)
            if data and data["date"]:
                self.display.draw_text(data["date"])
                output = numpy.int32(data["magnitude"] * 1000000000) + "|" + 0x00
                self.serial.write(output)
