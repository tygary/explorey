import json
import time
import RPi.GPIO as GPIO

from lighting.PixelControl import OverlayedPixelControl
from lighting.Colors import Colors, get_grb_color
from lighting.routines import Routines
from mqtt.MqttClient import MqttClient
from bank.FoundersBoxSoundSystem import FoundersBoxSoundSystem
from timemachine.Levers import Levers
# from timemachine.Button import Button


MQTT_EVENT_FOUNDER = "founder"

EVENT_LEVERS_CHANGED = "levers_changed"

MODE_CLOSED = 0
MODE_OPEN = 1


LED_COUNT = 50
BOTTOM_PIXELS = range(0, 50)

UNLOCK_TIMEOUT_S = 10

LOCK_PIN = 20


class FoundersBox(object):
    id = "founders_box"
    mode = MODE_CLOSED
    raw_lever_values = [0, 0, 0]
    magnitudes = [0, 0, 0]
    lock_time = 0

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.mqtt = MqttClient()
        self.levers = Levers(self.__on_lever_change, self.__on_button_change)
        self.mqtt.listen(self.__parse_mqtt_event)
        self.sound = FoundersBoxSoundSystem()
        self.pixels = OverlayedPixelControl(led_count=LED_COUNT, led_brightness=70, led_pin=21)
        GPIO.setup(LOCK_PIN, GPIO.OUT)
        self._update_light_routines()
        self.reset()

    def __on_lever_change(self, lever_id, value):
        if lever_id != 1:
            return
        raw_lever_value = self.raw_lever_values[lever_id]
        if raw_lever_value != value:
            # print(f"Got lever {id} change to {value}")
            modified_value = value * 100 * -1
            modified_prev_value = raw_lever_value * 100 * -1
            if abs(modified_value - modified_prev_value) > 2:
                rounded_value = round(modified_value)
                self.raw_lever_values[lever_id] = value
                self.magnitudes[lever_id] = rounded_value * 10
                print(f"magnitudes: {self.magnitudes}")
                self.sound.play_lever()
                self.__on_change_data()

    def __on_change_data(self):
        data = {
            "event": "economy_changed",
            "magnitudes": self.magnitudes
        }
        self.mqtt.publish(json.dumps(data))

    def __on_button_change(self, id, value):
        print(f"Got button {id} change to {value}")

    def _update_light_routines(self):
        if self.mode is MODE_CLOSED:
            self.light_routines = [
                Routines.BleuRoutine(self.pixels, BOTTOM_PIXELS),
            ]
        elif self.mode is MODE_OPEN:
            self.light_routines = [
                Routines.RainbowRoutine(self.pixels, BOTTOM_PIXELS, brightness=0.5),
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
            print("Artifact Failed parsing event", event, e)

    def unlock(self):
        print("Unlocking")
        self.lock_time = time.time() + UNLOCK_TIMEOUT_S
        self.mode = MODE_OPEN
        GPIO.output(LOCK_PIN, GPIO.HIGH)
        self._update_light_routines()

    def lock(self):
        print("Locking")
        self.lock_time = 0
        self.mode = MODE_CLOSED
        GPIO.output(LOCK_PIN, GPIO.LOW)
        self._update_light_routines()
        self.sound.play_open()

    def reset(self):
        print("Resetting")
        self.mode = MODE_CLOSED
        self.raw_lever_values = [0, 0, 0]
        self.magnitudes = [0, 0, 0]
        self.lock_time = 0
        self.lock()
        self._update_light_routines()
        self.sound.play_background()

    def update(self):
        self.levers.update()
        if self.lock_time > 0 and self.lock_time < time.time():
            print("Timed out, locking")
            self.lock()
        for routine in self.light_routines:
            routine.tick() 
        self.pixels.render()
        self.mqtt.publish_batch()
