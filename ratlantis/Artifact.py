import json

from lighting.Routine import *
from mqtt.MqttClient import MqttClient

CARD_FOUND = "cardFound"
CARD_REMOVED = "cardRemoved"


class Artifact(object):
    id = None
    mqtt = None
    is_attached = False
    is_activated = False
    current_rfid = None
    light_routine = None
    light_addresses = None
    pixels = None
    on_change = None

    def __init__(self, mqtt, pixels, light_addresses, id, on_change):
        self.mqtt = mqtt
        self.pixels = pixels
        self.light_addresses = light_addresses
        self.id = id
        self.on_change = on_change

        self.stop()
        self.mqtt.listen(self.__parse_mqtt_event)

    def __parse_mqtt_event(self, event):
        data = json.loads(event)
        if data and data["event"]:
            event = data["event"]
            reader_name = data["reader"]
            card_id = data["card"]
            if reader_name == self.id:
                if event == CARD_FOUND:
                    self.__on_card_detected(card_id)
                elif event == CARD_REMOVED:
                    self.__on_card_removed()

    def __on_card_detected(self, card):
        self.current_rfid = card
        self.on_change(self)

    def __on_card_removed(self):
        self.current_rfid = None
        self.is_attached = False
        self.on_change(self.id)

    def pulse_color(self, color_index):
        self.light_routine = FireRoutine(self.pixels, self.light_addresses, color_index)

    def wave(self, color):
        self.light_routine = WaveRoutine(self.pixels, self.light_addresses, [color])

    def stop(self):
        self.light_routine = BlackoutRoutine(self.pixels, self.light_addresses)

    def update(self):
        self.light_routine.tick()

