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
from timemachine.Button import Button
from bank.BeanDispenser import BeanDispenser

MQTT_EVENT_LEVERS_CHANGED = "levers_changed"

MODE_READY = "ready"
MODE_SCANNING = "scanning"

LED_COUNT = 50
BOTTOM_PIXELS = range(0, 50)

TIME_BETWEEN_INTEREST_S = 30

BEAN_CHUTE_PIN = 17
BEAN_DISPENSER_PIN = 4

class ATMMachine(object):
    id = "atm_machine"

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.lever_magnitudes = [0, 0, 0]
        self.mode = MODE_READY
        self.is_scanning = False
        self.next_interest_time = 0
        self.beans_deposited = 0
        self.deposit_success_cb = None
        
        self.mqtt = MqttClient()
        self.mqtt.listen(self.__parse_mqtt_event)
        self.printer = AccountPrinter()
        self.atm = ATM()
        self.dispenser = BeanDispenser(pin=BEAN_DISPENSER_PIN)
        self.scanner = FormScanner()
        self.bean_chute_trigger = Button(BEAN_CHUTE_PIN, callback=self._bean_detected, delay=0, pullup=True)
        self.ui = UiApp(self.atm, self.printer, start_scan=self.start_scan, cancel_scan=self.cancel_scan, start_deposit=self.start_deposit, cancel_deposit=self.cancel_deposit, dispense_beans=self.dispense_beans, get_interest_rate=self.get_interest_rate, get_exchange_rate=self.get_exchange_rate)
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
        print("Starting scan for document type:", document_type)
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
        if self.scan_success_cb:
            self.scan_success_cb(form_info)   
        self.scan_failure_cb = None
        self.scan_success_cb = None


    def start_deposit(self, success_cb, failure_cb):
        self.deposit_success_cb = success_cb
        self.deposit_failure_cb = failure_cb
        self.beans_deposited = 0

    def cancel_deposit(self):
        self.beans_deposited = 0
        self.deposit_success_cb = None
        self.deposit_failure_cb = None

    def _bean_detected(self):
        print("Bean detected in chute", self.beans_deposited)
        self.beans_deposited += 1
        if self.deposit_success_cb:
            self.deposit_success_cb(self.beans_deposited)

    def dispense_beans(self, amount):
        if amount <= 0:
            print("Invalid amount to dispense:", amount)
            return
        lumps = amount // 20
        self.dispenser.dispense(1)
        print(f"Dispensing {amount} beans in {lumps} lumps...")

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
                    print("Got Event", event, data)
                    if event == MQTT_EVENT_LEVERS_CHANGED:
                        self.lever_magnitudes = data["magnitude"]
                        print("Lever magnitudes", self.lever_magnitudes)
                        # self._update_light_routines()
        except Exception as e:
            print("ATM Machine Failed parsing event", event, e)

    def get_interest_rate(self):
        magnitude = self.lever_magnitudes[0]
        max_interest_rate = 0.05
        min_interest_rate = -0.02

        # TODO - get interest rate from lever
        return 0.05

    # Rate of exchange of X bean bucks to 1 bean
    def get_exchange_rate(self):
        magnitude = self.lever_magnitudes[1]
        max_exchange_rate = 5
        min_exchange_rate = 1
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
        self.bean_chute_trigger.tick()
        self.dispenser.update()
        # for routine in self.light_routines:
        #     routine.tick() 
        # self.pixels.render()
        self.mqtt.publish_batch()
