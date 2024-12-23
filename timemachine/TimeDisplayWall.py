import json
import numpy
from datetime import datetime, timedelta

from lighting.PixelDisplay import PixelDisplay
from mqtt.MqttClient import MqttClient
from timemachine.UsbSerial import UsbSerial
from timemachine.OscilloscopeSoundSystem import OscilloscopeSoundSystem
from timemachine.Button import Button
from timemachine.TimePrinter import TimeRecordPrinter

START = datetime(1000, 1, 1, 0, 0, 0)

PRINT_BUTTON = 25
PRINT_BUTTON_LIGHT = 24


class TimeDisplayWall(object):
    display = PixelDisplay()
    mqtt = MqttClient()
    osounds = OscilloscopeSoundSystem()
    serial = UsbSerial("/dev/ttyACM0")
    last_magnitude = 0
    print_button = None
    printer = TimeRecordPrinter()
    date = START
    date_string = ""

    def __init__(self):
        self.mqtt.listen(self.__on_event)
        # self.serial.disable()
        self.print_button = Button(PRINT_BUTTON, PRINT_BUTTON_LIGHT, self.__on_print_button)
        self.print_button.set_light(False)

    def __on_print_button(self):
        print("Print button")
        self.printer.printTimeRecord(self.date, self.date_string)

    def __on_event(self, event):
        #print(f"Got Event: {event}")
        #print(self.serial.read())
        if event:
            try:
                data = json.loads(event)
                if data["event"] == "timechange":
                    self.osounds.update_sounds(data["active"] is True)
                    if data["date"] and (data["active"] is True or data["startup"] is True):
                        date = START + timedelta(seconds=data["timestamp"])
                        self.date = date
                        self.date_string = data["date"]
                        self.display.draw_text(data["date"])
                    active = 1 if data["active"] is True else 0
                    self.print_button.set_light(data["active"])
                    magnitude = data["magnitude"]
                    color_mode = data["color_mode"]
                    freq_mode = data["freq_mode"]
                    output = numpy.int16(magnitude).tobytes() + numpy.uint8(color_mode).tobytes() + numpy.uint8(
                        freq_mode).tobytes() + numpy.uint8(active).tobytes()
                    self.serial.write(output)
                        # print(output)
                    if data["active"] is False and data["startup"] is False:
                        self.display.draw_text("")
            except Exception as err:
                print(err)
