import json
import numpy
from datetime import datetime, timedelta

from lighting.PixelDisplay import PixelDisplay
from mqtt.MqttClient import MqttClient
from timemachine.UsbSerial import UsbSerial
from timemachine.OscilloscopeSoundSystem import OscilloscopeSoundSystem
from timemachine.ImageViewer import ImageViewer

START = datetime(1000, 1, 1, 0, 0, 0)


class TimeDisplay(object):
    display = PixelDisplay()
    mqtt = MqttClient()
    osounds = OscilloscopeSoundSystem()
    serial = UsbSerial("/dev/ttyACM0")
    viewer = ImageViewer()
    last_magnitude = 0

    def __init__(self):
        self.mqtt.listen(self.__on_event)
        self.serial.disable()

    def __on_event(self, event):
        print(f"Got Event: {event}")
        print(self.serial.read())
        if event:
            data = json.loads(event)
            self.osounds.update_sounds(data["active"] is True)
            if data["date"]:
                date = START + timedelta(seconds=data["timestamp"])
                self.viewer.update(date, data["date"])
                self.display.draw_text(data["date"])
                magnitude = data["magnitude"]
                if self.last_magnitude != magnitude:
                    output = numpy.int16(magnitude).tobytes() + numpy.uint8(0).tobytes()
                    print(output)
                    self.serial.write(output)
                    self.last_magnitude = magnitude
