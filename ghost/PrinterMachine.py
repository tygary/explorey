import json
import random
import time
import RPi.GPIO as GPIO

from lighting.PixelControl import PixelControl
from lighting.Colors import Colors
from lighting.routines import Routines
from mqtt.MqttClient import MqttClient

from ghost.GhostPrinter import GhostPrinter

from timemachine.Button import Button


EVENT_CARD_FOUND = "cardFound"
EVENT_CARD_REMOVED = "cardRemoved"
EVENT_FINISHED_BOOT = "finishedBoot"
EVENT_GHOST_UPDATE = "ghostUpdate"
EVENT_RESET_COMMAND = "reset"
EVENT_OPEN_DOOR_COMMAND = "openDoor"
EVENT_WRITE_RFID_COMMAND = "writeRfid"

BUTTON_PIN = 1

MODE_OFF = 0
MODE_SCANNING = 1
MODE_READY_TO_PRINT = 2

TIME_BEFORE_READY_TO_PRINT = 5


class PrinterMachine(object):
    id = "printer"
    current_rfid = None
    light_routines = []
    next_event_time = 0
    mode = MODE_OFF

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.mqtt = MqttClient()
        self.printer = GhostPrinter()
        self.button = Button(BUTTON_PIN, callback=self.button_pressed)
        self.mqtt.listen(self.__parse_mqtt_event)

    def button_pressed(self):
        print("Button pressed")
        if self.mode is MODE_READY_TO_PRINT and self.current_rfid:
            self.mode = MODE_OFF
            self.printer.print_ghost(self.current_rfid)
            self.mqtt.queue_in_batch_publish({
                "event": EVENT_GHOST_UPDATE,
                "reader": self.id,
                "id": self.id,
                "command": EVENT_WRITE_RFID_COMMAND,
            })

    def __parse_mqtt_event(self, event):
        try:
            events = json.loads(event)
            if not type(events) in (tuple, list):
                events = [events]
            for data in events:
                if data and data["event"]:
                    event = data["event"]
                    if event == EVENT_CARD_FOUND or event == EVENT_CARD_REMOVED or event == EVENT_FINISHED_BOOT:
                        reader_name = data["reader"]
                        if reader_name == self.id:
                            if event == EVENT_CARD_FOUND:
                                card_id = data["card"]
                                self.__on_card_detected(card_id)
                            elif event == EVENT_CARD_REMOVED:
                                self.__on_card_removed()
                            elif event == EVENT_FINISHED_BOOT:
                                pass
                                # Nothing yet
        except Exception as e:
            print("Artifact Failed parsing event", event, e)

    def __on_card_detected(self, card):
        print("Card detected", card)
        self.current_rfid = card
        self.mode = MODE_SCANNING
        self.next_event_time = time.time() + TIME_BEFORE_READY_TO_PRINT
        self.button.set_light(False)

    def __on_card_removed(self):
        print("card removed")
        self.current_rfid = None
        self.mode = MODE_OFF
        self.next_event_time = 0
        self.button.set_light(False)

    def update(self):
        if self.mode is MODE_SCANNING and self.next_event_time and self.next_event_time > time.time():
            self.mode = MODE_READY_TO_PRINT
            self.button.flash_light()

        self.button.tick()
