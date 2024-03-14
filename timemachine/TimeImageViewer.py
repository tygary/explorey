import json
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

from mqtt.MqttClient import MqttClient
from timemachine.ImageViewer import ImageViewer
from timemachine.TimeDmx import TimeDmx
from timemachine.Button import Button

START = datetime(1000, 1, 1, 0, 0, 0)

COUNTDOWN_BUTTON = 18  # ???
COUNTDOWN_BUTTON_LIGHT = 22  # ???


class TimeImageViewer(object):
    mqtt = MqttClient()
    viewer = ImageViewer()
    dmx = TimeDmx()
    # music = TimeMachineSoundSystem()
    date = START
    date_string = ""
    magnitude = 0
    data = None
    countdown_button = None

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.mqtt.listen(self.__on_event)
        self.countdown_button = Button(COUNTDOWN_BUTTON, COUNTDOWN_BUTTON_LIGHT, self.__on_countdown_button)
        self.countdown_button.set_light(True)
        print("Started TimeImageViewer")

    def __on_countdown_button(self):
        print("Starting Countdown")
        self.mqtt.publish(json.dumps({"event": "countdownButton"}))

    def tick(self):
        self.dmx.update()

    def __on_event(self, event):
        # print(f"Got Event: {event}")
        # print(self.serial.read())
        if event:
            try:
                data = json.loads(event)
                if data["event"] == "timechange":
                    self.data = data
                    self.dmx.change_mode(data["active"], data["startup"])
                    if data["date"]:
                        date = START + timedelta(seconds=data["timestamp"])
                        self.date = date
                        self.date_string = data["date"]

                        self.viewer.update(date, data["date"], data["active"])
            except Exception as err:
                print(err)
