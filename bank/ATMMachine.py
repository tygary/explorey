import json
import random
import time
import RPi.GPIO as GPIO

from lighting.PixelControl import OverlayedPixelControl
from lighting.Colors import Colors, get_grb_color
from lighting.routines import Routines
from mqtt.MqttClient import MqttClient
from bank.ATM import ATM

from timemachine.Levers import *
# from timemachine.Button import Button


MQTT_EVENT_LEVERS_CHANGED = "levers_changed"

MODE_READY = "ready"
MODE_SCANNING = "scanning"

LED_COUNT = 50
BOTTOM_PIXELS = range(0, 50)

TIME_BETWEEN_INTEREST_S = 30

class ATMMachine(object):
    id = "atm_machine"
    
    lever_magnitudes = [0, 0, 0]

    next_interest_time = 0

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.mqtt = MqttClient()
        self.mqtt.listen(self.__parse_mqtt_event)
        self.atm = ATM()
        self.pixels = OverlayedPixelControl(led_count=LED_COUNT, led_brightness=255)
        self._update_light_routines()
        self.reset()


    def _update_light_routines(self):
        if self.mode is MODE_READY:
            self.light_routines = [
                Routines.BlackoutRoutine(self.pixels, BOTTOM_PIXELS),
            ]
        elif self.mode is MODE_OPEN:
            self.light_routines = [
                Routines.ColorRoutine(self.pixels, BOTTOM_PIXELS, color=Colors.white),
            ]
        print("Updated light routines", self.mode)

    def __parse_mqtt_event(self, event):
        try:
            events = json.loads(event)
            if not type(events) in (tuple, list):
                events = [events]
            for data in events:
                if data and data["event"]:
                    event = data["event"]
                    if event == MQTT_EVENT_FOUNDER:
                        self.unlock()
        except Exception as e:
            print("ATM Machine Failed parsing event", event, e)

    def get_interest_rate(self):
        magnitude = self.lever_magnitudes[0]
        # TODO - get interest rate from lever
        return 0.05

    # Rate of exchange of X bean bucks to 1 bean
    def get_exchange_rate(self):
        magnitude = self.lever_magnitudes[1]
        # TODO - get exchange rate from lever
        return 2
  
    def reset(self):
        print("Resetting")
        self.mode = MODE_READY
        self.lever_magnitudes = [0, 0, 0]
        self.next_interest_time = time.time() + TIME_BETWEEN_INTEREST_S
        self._update_light_routines()

    def update(self):
        self.levers.update()
        if self.lock_time > 0 and self.lock_time < time.time():
            print("Timed out, locking")
            self.lock()
        for routine in self.light_routines:
            routine.tick() 
        self.pixels.render()
        self.mqtt.publish_batch()
