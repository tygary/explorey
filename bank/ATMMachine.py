import json
import time
import math
import RPi.GPIO as GPIO

from lighting.PixelControl import OverlayedPixelControl
from lighting.Colors import Colors, get_grb_color
from lighting.routines import Routines
from mqtt.MqttClient import MqttClient
from bank.ATM import ATM
from bank.ui.UI import UiApp
from bank.FormScanner import FormScanner, FormInfo
from bank.AccountPrinter import AccountPrinter
from timemachine.Button import Button
from bank.BeanDispenser import BeanDispenser

MQTT_EVENT_LEVERS_CHANGED = "economy_changed"

MODE_READY = "ready"
MODE_SCANNING = "scanning"

LED_COUNT = 1050
SIGN_PIXEL_WIDTH = 64
SIGN_PIXEL_HEIGHT = 8
NUM_SIGN_PIXELS = 1024

SIGN_BOTTOM_PIXELS = range(0, 512)
SIGN_TOP_PIXELS = range(512, 1024)

BOTTOM_PIXELS = range(NUM_SIGN_PIXELS, NUM_SIGN_PIXELS + 10)

TIME_BETWEEN_INTEREST_S = 60 * 20

BEAN_CHUTE_PIN = 17
BEAN_DISPENSER_PIN = 4

CHOSEN_LEVER_VALUE = 400
ECONOMY_UPDATE_INTERVAL = 60 * 2

FOUNDER_UPDATE_TIME_S = 60 * 60

class ATMMachine(object):
    id = "atm_machine"

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.lever_magnitudes = [0, 0, 0]
        self.mode = MODE_READY
        self.is_scanning = False
        self.next_interest_time = time.time() + TIME_BETWEEN_INTEREST_S
        self.beans_deposited = 0
        self.deposit_success_cb = None
        self.interest_rate = 0.05
        self.debt_interest_rate = 0.05
        self.exchange_rate = 2
        self.current_magnitude = 0
        self.bean_deposit_start = 0
        self.last_founder_update_time = 0
        self.last_economy_update = time.time()
        self.mqtt = MqttClient()
        self.mqtt.listen(self.__parse_mqtt_event)
        self.printer = AccountPrinter()
        self.atm = ATM()
        self.dispenser = BeanDispenser(pin=BEAN_DISPENSER_PIN)
        self.scanner = FormScanner()
        self.bean_chute_trigger = Button(BEAN_CHUTE_PIN, callback=self._bean_detected, delay=0, pullup=True)
        self.ui = UiApp(self.atm, self.printer, start_scan=self.start_scan, cancel_scan=self.cancel_scan, start_deposit=self.start_deposit, cancel_deposit=self.cancel_deposit, dispense_beans=self.dispense_beans, get_interest_rate=self.get_interest_rate, get_exchange_rate=self.get_exchange_rate, get_debt_interest_rate=self.get_debt_interest_rate)
        self.pixels = OverlayedPixelControl(led_count=LED_COUNT, led_brightness=255)
        self.reset()

    def start_scan(self, document_type, on_success, on_failure):
        if self.mode == MODE_SCANNING:
            print("Already scanning")
            self.scanner.stop_scanning()
        self.mode = MODE_SCANNING
        self._update_light_routines()
        self.render_lights()
        self.scan_success_cb = on_success
        self.scan_failure_cb = on_failure
        print("Starting scan for document type:", document_type)
        self.scanner.start_scanning(document_type, self.finish_scanning)
        print("Starting scan")

    def cancel_scan(self):
        self.scanner.stop_scanning()
        if self.mode == MODE_SCANNING:
            self.mode = MODE_READY
            self._update_light_routines()
            self.render_lights()
            self.scan_failure_cb = None
            self.scan_success_cb = None
            print("Cancelled scan")
        else:
            print("Not scanning, cannot cancel")

    def finish_scanning(self, form_info: FormInfo):
        self.mode = MODE_READY
        self.scanner.stop_scanning()
        self._update_light_routines()
        self.render_lights()
        print("Finished scanning", form_info)
        if self.scan_success_cb:
            self.scan_success_cb(form_info)   
        self.scan_failure_cb = None
        self.scan_success_cb = None

    def start_deposit(self, success_cb, failure_cb):
        self.deposit_success_cb = success_cb
        self.deposit_failure_cb = failure_cb
        self.bean_deposit_start = time.time()
        self.beans_deposited = 0

    def cancel_deposit(self):
        self.beans_deposited = 0
        self.bean_deposit_start = 0
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
        lumps = math.ceil(amount / 20)
        self.dispenser.dispense(lumps)
        print(f"Dispensing {amount} beans in {lumps} lumps...")

    def render_lights(self):
        try:
            percentage = (1000 - self.lever_magnitudes[1]) / 2000
            print("Rendering lights", self.mode, self.lever_magnitudes, percentage)
            self.light_routines[1].tick()
            for routine in self.light_routines[0].routines:
                routine.update_percentage(percentage)
                routine.tick()
            self.pixels.render()
        except Exception as e:
            print("ATM Machine Failed rendering lights", e)

    def _update_light_routines(self):
        self.light_routines = [
            Routines.MultiRoutine([
                Routines.GaugeRoutine(self.pixels, SIGN_TOP_PIXELS, color=[0, 50, 0]),
                Routines.GaugeRoutine(self.pixels, SIGN_BOTTOM_PIXELS, color=[0, 50, 0]),
            ])
        ]
        if self.mode is MODE_READY:
            self.light_routines.append(Routines.BlackoutRoutine(self.pixels, BOTTOM_PIXELS))
        elif self.mode is MODE_SCANNING:
            self.light_routines.append(Routines.ColorRoutine(self.pixels, BOTTOM_PIXELS, color=Colors.white))
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
                        self.lever_magnitudes = data["magnitudes"]
                        print("Lever magnitudes", self.lever_magnitudes)
                        self.update_economy(self.lever_magnitudes)
        except Exception as e:
            print("ATM Machine Failed parsing event", event, e)

    def update_economy(self, lever_magnitudes):
        print("Lever Values: ", lever_magnitudes)
        magnitude = lever_magnitudes[1]
        magnitude_normalized = (magnitude + 1000) / 2000
        if (magnitude_normalized > self.current_magnitude):
            amount = min(abs(magnitude_normalized - self.current_magnitude), 0.1)
            self.current_magnitude += amount
        else:
            amount = min(abs(magnitude_normalized - self.current_magnitude), 0.1)
            self.current_magnitude -= amount
        magnitude_normalized = self.current_magnitude
        magnitude = magnitude_normalized * 2000 - 1000
        self.lever_magnitudes = [0, magnitude, 0]
        print("Economy current magnitude: ", self.current_magnitude)

        self.atm.set_starting_balance(int(magnitude_normalized * 50))  # Between 0 and 100
        print("Setting starting balance to", self.atm.starting_balance)

        self.atm.set_withdrawl_amount(int(20 + (magnitude_normalized * 40)))  # Between 20 and 100
        print("Setting withdrawl amount to", self.atm.withdrawl_amount)

        max_interest_rate = 0.03
        min_interest_rate = -0.07
        self.interest_rate = round(min_interest_rate + (max_interest_rate - min_interest_rate) * magnitude_normalized, 4)
        print("Setting interest rate to", self.interest_rate)

        max_exchange_rate = 5
        min_exchange_rate = 0.1
        self.exchange_rate = round(min_exchange_rate + (max_exchange_rate - min_exchange_rate) * (1 - magnitude_normalized), 2)
        self.atm.set_exchange_rate(self.exchange_rate)
        print("Setting exchange rate to", self.exchange_rate)

        max_debt_interest_rate = 0.05
        min_debt_interest_rate = 0.01
        self.debt_interest_rate = round(min_debt_interest_rate + (max_debt_interest_rate - min_debt_interest_rate) * (1 - magnitude_normalized), 4)
        print("Setting debt interest rate to", self.debt_interest_rate)
        self.render_lights()


    def get_interest_rate(self):
        return self.interest_rate
    
    def get_debt_interest_rate(self):
        return self.debt_interest_rate

    # Rate of exchange of X bean bucks to 1 bean
    def get_exchange_rate(self):
        return self.exchange_rate
  
    def reset(self):
        print("Resetting")
        self.mode = MODE_READY
        self.atm.apply_interest(self.interest_rate, self.debt_interest_rate)
        self._update_light_routines()
        self.render_lights()
        self.lever_magnitudes = [0, 0, 0]
        self.next_interest_time = time.time() + TIME_BETWEEN_INTEREST_S
        # self._update_light_routines()

    def start(self):
        self.ui.start(self.update)

    def update(self):
        try:
            now = time.time()
            if self.bean_deposit_start > 0 and now >= self.bean_deposit_start + 10:
                self.bean_deposit_start = 0
                if self.deposit_success_cb:
                    self.deposit_success_cb(500)
                    # self.deposit_success_cb(200)
                    # self.deposit_success_cb(200)
            if now >= self.next_interest_time:
                self.next_interest_time = time.time() + TIME_BETWEEN_INTEREST_S
                print("Applying interest rate", self.interest_rate)
                self.atm.apply_interest(self.interest_rate, self.debt_interest_rate, self.current_magnitude)
            if now >= self.last_economy_update + ECONOMY_UPDATE_INTERVAL:
                self.last_economy_update = now
                self.update_economy([0, CHOSEN_LEVER_VALUE, 0])
            if now >= self.last_founder_update_time + FOUNDER_UPDATE_TIME_S:
                self.last_founder_update_time = now
                founder = self.atm.get_account(46793)
                founder.balance = 123456789
                self.atm.update_account(founder)

                gotturd = self.atm.get_account(34001)
                gotturd.balance = 252971
                self.atm.update_account(gotturd)

                squeezy = self.atm.get_account(44808)
                squeezy.balance = 219211
                self.atm.update_account(squeezy)

                gobleena = self.atm.get_account(54531)
                gobleena.balance = 123121
                self.atm.update_account(gobleena)
        except Exception as e:
            print("Error applying interest rate", e)
        try:
            self.scanner.update()
            self.bean_chute_trigger.tick()
            self.dispenser.update()
        except Exception as e:
            print("Error updating scanner or bean chute trigger", e)
        self.mqtt.publish_batch()
