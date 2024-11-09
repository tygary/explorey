import json
import random
import time
import RPi.GPIO as GPIO

from lighting.PixelControl import OverlayedPixelControl
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
# EVENT_OPEN_DOOR_COMMAND = "openDoor"
# EVENT_WRITE_RFID_COMMAND = "writeRfid"
EVENT_SET_RUNNING = "setRunning"
EVENT_SET_FINISHED = "setFinished"

EVENT_READY_TO_PRINT = "ready_to_print"

BUTTON_PIN = 22
BUTTON_LIGHT_PIN = 23

MODE_OFF = 0
MODE_SCANNING = 1
MODE_READY_TO_PRINT = 2
MODE_FINISHED = 3

TIME_BEFORE_READY_TO_PRINT = 10
TIME_BEFORE_RESETTING = 10
PRINT_READY_TIMEOUT_TIME = 10


TUBE_INNER_START_PIXEL = 0
TUBE_INNER_NUM_PIXELS = 192
TUBE_OUTER_START_PIXEL = TUBE_INNER_START_PIXEL + TUBE_INNER_NUM_PIXELS
TUBE_OUTER_NUM_PIXELS = 320
DIORAMA_WALL_START_PIXEL = TUBE_OUTER_START_PIXEL + TUBE_OUTER_NUM_PIXELS
DIORAMA_WALL_NUM_PIXELS = 50
DIORAMA_FIBER_START_PIXEL = DIORAMA_WALL_START_PIXEL + DIORAMA_WALL_NUM_PIXELS + 1
DIORAMA_FIBER_NUM_PIXELS = 4

TUBE_INNER_PIXELS_A_END = TUBE_INNER_START_PIXEL + TUBE_INNER_NUM_PIXELS // 3
TUBE_INNER_PIXELS_A = list(range(TUBE_INNER_START_PIXEL, TUBE_INNER_PIXELS_A_END))
TUBE_INNER_PIXELS_B_START = TUBE_INNER_PIXELS_A_END
TUBE_INNER_PIXELS_B_END = (TUBE_INNER_NUM_PIXELS - TUBE_INNER_PIXELS_A_END) // 2 + TUBE_INNER_PIXELS_B_START
TUBE_INNER_PIXELS_B = list(range(TUBE_INNER_PIXELS_B_START, TUBE_INNER_PIXELS_B_END))
TUBE_INNER_PIXELS_B.reverse()
TUBE_INNER_PIXELS_C = list(range(TUBE_INNER_PIXELS_B_END, TUBE_INNER_NUM_PIXELS))


TUBE_INNER_PIXELS = TUBE_INNER_PIXELS_A + TUBE_INNER_PIXELS_B + TUBE_INNER_PIXELS_C
TUBE_OUTER_PIXELS = list(range(TUBE_OUTER_START_PIXEL, TUBE_OUTER_START_PIXEL + TUBE_OUTER_NUM_PIXELS))
DIORAMA_WALL_PIXELS = list(range(DIORAMA_WALL_START_PIXEL, DIORAMA_WALL_START_PIXEL + DIORAMA_WALL_NUM_PIXELS))
DIORAMA_FIBER_PIXELS = list(range(DIORAMA_FIBER_START_PIXEL, DIORAMA_FIBER_START_PIXEL + DIORAMA_FIBER_NUM_PIXELS))


class PrinterMachine(object):
    id = "printer"
    current_rfid = None
    light_routines = []
    next_event_time = 0
    next_reset_time = 0
    mode = MODE_OFF

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.mqtt = MqttClient()
        self.printer = GhostPrinter()
        self.button = Button(BUTTON_PIN, BUTTON_LIGHT_PIN, callback=self.button_pressed, pullup=True)
        self.mqtt.listen(self.__parse_mqtt_event)
        self.pixels = OverlayedPixelControl(led_count=DIORAMA_FIBER_START_PIXEL + DIORAMA_FIBER_NUM_PIXELS, led_brightness=255)
        self._update_light_routines()

    def _update_light_routines(self):
        if self.mode is MODE_OFF:
            self.light_routines = [
                Routines.BlackoutRoutine(self.pixels, TUBE_INNER_PIXELS),
                Routines.BlackoutRoutine(self.pixels, TUBE_OUTER_PIXELS),
                Routines.BlackoutRoutine(self.pixels, DIORAMA_WALL_PIXELS),
                Routines.BleuRoutine(self.pixels, DIORAMA_FIBER_PIXELS),
            ]
        elif self.mode is MODE_SCANNING:
            self.light_routines = [
                Routines.WaveRoutine(self.pixels, TUBE_INNER_PIXELS_A, [Colors.light_green], pixel_wait_time=0, wave_wait_time=0, brightness=0.7),
                Routines.WaveRoutine(self.pixels, TUBE_INNER_PIXELS_B, [Colors.yellow], pixel_wait_time=0, wave_wait_time=0, brightness=0.7),
                Routines.WaveRoutine(self.pixels, TUBE_INNER_PIXELS_C, [Colors.orange], pixel_wait_time=0, wave_wait_time=0, brightness=1.0),
                Routines.PulseRoutine(self.pixels, TUBE_INNER_PIXELS, Colors.mid_green, 0.5, brightness=0.2),

                Routines.WaveRoutine(self.pixels, TUBE_OUTER_PIXELS, [Colors.light_green, Colors.yellow], wave_wait_time=0, brightness=0.7),
                
                Routines.MushroomRoutine(self.pixels, DIORAMA_WALL_PIXELS, brightness=0.5),
                Routines.PulseRoutine(self.pixels, DIORAMA_WALL_PIXELS, Colors.light_green, 0.5, brightness=0.3),
                
                Routines.RainbowRoutine(self.pixels, DIORAMA_FIBER_PIXELS, brightness=1),
                Routines.PulseRoutine(self.pixels, DIORAMA_FIBER_PIXELS, Colors.light_green, 0.5, brightness=0.5),
            ]
        elif self.mode is MODE_READY_TO_PRINT:
            self.light_routines = [
                Routines.BleuRoutine(self.pixels, TUBE_INNER_PIXELS, brightness=0.25),
                Routines.WaveRoutine(self.pixels, TUBE_INNER_PIXELS, [Colors.mid_green, Colors.orange], wave_wait_time=0, brightness=0.25),
                Routines.PulseRoutine(self.pixels, TUBE_INNER_PIXELS, Colors.light_green, 0.5, brightness=0.25),

                Routines.MushroomRoutine(self.pixels, TUBE_OUTER_PIXELS, brightness=0.25),
                Routines.WaveRoutine(self.pixels, TUBE_OUTER_PIXELS, [Colors.purple, Colors.soft_blue], wave_wait_time=10, brightness=0.25),
                Routines.PulseRoutine(self.pixels, TUBE_OUTER_PIXELS, Colors.purple, 0.3, brightness=0.25),
                
                Routines.MushroomRoutine(self.pixels, DIORAMA_WALL_PIXELS, brightness=0.3),
                Routines.RandomPulseRoutine(self.pixels, DIORAMA_WALL_PIXELS, brightness=0.5),

                Routines.BleuRoutine(self.pixels, DIORAMA_FIBER_PIXELS),
                Routines.PulseRoutine(self.pixels, DIORAMA_FIBER_PIXELS, Colors.light_green, 0.5, brightness=0.5),
            ]
        elif self.mode is MODE_FINISHED:
            self.light_routines = [
                Routines.BlackoutRoutine(self.pixels, TUBE_INNER_PIXELS),
                Routines.BlackoutRoutine(self.pixels, TUBE_OUTER_PIXELS),
                Routines.MushroomRoutine(self.pixels, DIORAMA_WALL_PIXELS, brightness=0.5),
                Routines.BleuRoutine(self.pixels, DIORAMA_FIBER_PIXELS),
            ]
        print("Updated light routines", self.mode)

    def button_pressed(self):
        print("Button pressed")
        if self.mode is MODE_READY_TO_PRINT and self.current_rfid:
            self.mode = MODE_FINISHED
            self.next_reset_time = time.time() + TIME_BEFORE_RESETTING
            self._update_light_routines()
            self.printer.print_ghost(self.current_rfid)
            self.current_rfid = None
            self.button.set_light(False)
            self.mqtt.queue_in_batch_publish({
                "event": EVENT_GHOST_UPDATE,
                "reader": self.id,
                "id": self.id,
                "command": EVENT_SET_FINISHED,
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
                            print("Got MQTT Event", event)
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
        if self.current_rfid != card:
            self.current_rfid = card
            self.mode = MODE_SCANNING
            print("Scanning trash")
            self.next_event_time = time.time() + TIME_BEFORE_READY_TO_PRINT
            self.button.set_light(False)
            self._update_light_routines()
            self.mqtt.queue_in_batch_publish({
                "event": EVENT_GHOST_UPDATE,
                "reader": self.id,
                "id": self.id,
                "command": EVENT_SET_RUNNING,
            })

    def __on_card_removed(self):
        print("card removed")
        if self.mode not in [MODE_OFF, MODE_SCANNING, MODE_FINISHED]:
            self.next_reset_time = time.time() + PRINT_READY_TIMEOUT_TIME
        # self.current_rfid = None
        # self.mode = MODE_OFF
        # self.next_event_time = 0
        # self.button.set_light(False)

    def update(self):
        if self.next_reset_time > 0 and self.next_reset_time < time.time():
            print("Timed out, resetting")
            self.mode = MODE_OFF
            self.next_reset_time = 0
            self.button.set_light(False)
            self.current_rfid = None
            self._update_light_routines()
            self.mqtt.queue_in_batch_publish({
                "event": EVENT_GHOST_UPDATE,
                "reader": self.id,
                "id": self.id,
                "command": EVENT_RESET_COMMAND,
            })
        if self.mode is MODE_SCANNING and self.next_event_time > 0 and self.next_event_time < time.time():
            print("Ready to print")
            self.mode = MODE_READY_TO_PRINT
            self.next_event_time = 0
            self.next_reset_time = 0
            # self.next_reset_time = time.time() + PRINT_READY_TIMEOUT_TIME
            self.button.flash_light()
            self.mqtt.queue_in_batch_publish({
                "event": EVENT_GHOST_UPDATE,
                "reader": self.id,
                "id": self.id,
                "command": EVENT_READY_TO_PRINT,
            })
            self._update_light_routines()
        for routine in self.light_routines:
            routine.tick()
        self.button.tick()
        self.pixels.render()
        self.mqtt.publish_batch()