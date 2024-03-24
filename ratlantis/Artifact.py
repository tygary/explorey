import json

from lighting.routines import Routines

CARD_FOUND = "cardFound"
CARD_REMOVED = "cardRemoved"


class Artifact(object):
    id = None
    mqtt = None
    is_attached = False
    is_activated = False
    current_rfid = None
    ring_light_routine = None
    ring_light_addresses = None
    pixels = None
    on_change = None

    def __init__(self, mqtt, pixels, ring_light_addresses, artifact_id, on_change):
        self.mqtt = mqtt
        self.pixels = pixels
        self.ring_light_addresses = ring_light_addresses
        self.id = artifact_id
        self.on_change = on_change

        self.ring_stop()
        self.mqtt.listen(self.__parse_mqtt_event)

    def __parse_mqtt_event(self, event):
        data = json.loads(event)
        if data and data["event"]:
            print(data)
            event = data["event"]
            reader_name = data["reader"]
            card_id = data["card"]
            if reader_name == self.id:
                if event == CARD_FOUND:
                    self.__on_card_detected(card_id)
                elif event == CARD_REMOVED:
                    self.__on_card_removed()

    def __on_card_detected(self, card):
        print("Card deected", card)
        self.current_rfid = card
        self.on_change(self)

    def __on_card_removed(self):
        print("card removed")
        self.current_rfid = None
        self.is_attached = False
        self.on_change(self)

    def ring_pulse_color(self, color_index):
        self.ring_light_routine = Routines.FireRoutine(self.pixels, self.ring_light_addresses, color_index)

    def ring_wave(self, color):
        self.ring_light_routine = Routines.WaveRoutine(self.pixels, self.ring_light_addresses, [color])

    def ring_stop(self):
        self.ring_light_routine = Routines.BlackoutRoutine(self.pixels, self.ring_light_addresses)

    def update(self):
        self.ring_light_routine.tick()

