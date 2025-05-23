import json
import random
import time
import RPi.GPIO as GPIO

from lighting.PixelControl import OverlayedPixelControl
from lighting.Colors import Colors, get_grb_color
from lighting.routines import Routines
from mqtt.MqttClient import MqttClient
from bank.ATM import ATM
from bank.UI import UiApp
from bank.FormScanner import FormScanner, FormInfo
from bank.AccountPrinter import AccountPrinter

MQTT_EVENT_LEVERS_CHANGED = "levers_changed"

MODE_READY = "ready"
MODE_SCANNING = "scanning"

LED_COUNT = 50
BOTTOM_PIXELS = range(0, 50)

TIME_BETWEEN_INTEREST_S = 30

class ATMMachine(object):
    id = "atm_machine"

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.lever_magnitudes = [0, 0, 0]
        self.mode = MODE_READY
        self.is_scanning = False
        self.next_interest_time = 0
        
        self.mqtt = MqttClient()
        self.mqtt.listen(self.__parse_mqtt_event)
        self.printer = AccountPrinter()
        self.atm = ATM()
        self.scanner = FormScanner()
        self.ui = UiApp(self.atm, self.printer, self.start_scan, self.cancel_scan)
        # self.pixels = OverlayedPixelControl(led_count=LED_COUNT, led_brightness=255)
        # self._update_light_routines()
        self.reset()

    def start_scan(self, document_type, on_success, on_failure):
        if self.mode == MODE_SCANNING:
            print("Already scanning")
            self.scanner.stop_scanning()
        self.mode = MODE_SCANNING
        self.scan_success_cb = on_success
        self.scan_failure_cb = on_failure
        self.scanner.start_scanning(document_type, self.finish_scanning)
        # self._update_light_routines()
        print("Starting scan")

    def cancel_scan(self):
        if self.mode == MODE_SCANNING:
            self.scanner.stop_scanning()
            self.mode = MODE_READY
            self.scan_failure_cb = None
            self.scan_success_cb = None
            # self._update_light_routines()
            print("Cancelled scan")
        else:
            print("Not scanning, cannot cancel")

    def finish_scanning(self, form_info: FormInfo):
        self.mode = MODE_READY
        self.scanner.stop_scanning()
        # self._update_light_routines()
        print("Finished scanning", form_info)
        self.scan_success_cb(form_info)   
        self.scan_failure_cb = None
        self.scan_success_cb = None

    def _update_light_routines(self):
        if self.mode is MODE_READY:
            self.light_routines = [
                Routines.BlackoutRoutine(self.pixels, BOTTOM_PIXELS),
            ]
        elif self.mode is MODE_SCANNING:
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
                    if event == MQTT_EVENT_LEVERS_CHANGED:
                        self.lever_magnitudes = data["magnitude"]
                        print("Lever magnitudes", self.lever_magnitudes)
                        # self._update_light_routines()
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
        # self._update_light_routines()

    def start(self):
        self.ui.start(self.update)

    def update(self):
        self.scanner.update()
        # for routine in self.light_routines:
        #     routine.tick() 
        # self.pixels.render()
        self.mqtt.publish_batch()
