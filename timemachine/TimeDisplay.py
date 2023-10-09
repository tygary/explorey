import json

import numpy

from lighting.PixelDisplay import PixelDisplay
from mqtt.MqttClient import MqttClient
from lighting.UsbSerial import UsbSerial


class TimeDisplay(object):
    display = PixelDisplay()
    mqtt = MqttClient()
    serial = UsbSerial("/dev/ttyACM0")
    last_magnitude = 0

    def __init__(self):
        self.mqtt.listen(self.__on_event)

    def __on_event(self, event):
        print(f"Got Event: {event}")
        print(self.serial.read())
        if event:
            data = json.loads(event)
            if data and data["date"]:
                self.display.draw_text(data["date"])
                magnitude = data["magnitude"]
                if self.last_magnitude != magnitude:
                    output = numpy.int16(magnitude).tobytes() + numpy.uint8(0).tobytes()
                    print(output)
                    self.serial.write(output)
                    self.last_magnitude = magnitude
