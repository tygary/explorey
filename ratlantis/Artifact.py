import json

from lighting.Colors import Colors
from lighting.routines import Routines

CARD_FOUND = "cardFound"
CARD_REMOVED = "cardRemoved"


class Artifact(object):
    id = None
    mqtt = None
    current_rfid = None
    desired_rfid = None
    on_change = None

    def __init__(self, mqtt, artifact_id, on_change):
        self.mqtt = mqtt
        self.id = artifact_id
        self.on_change = on_change

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
        print("Card detected", card)
        self.current_rfid = card
        self.on_change(self)

    def __on_card_removed(self):
        print("card removed")
        self.current_rfid = None
        self.is_attached = False
        self.on_change(self)

    def set_pending_vine(self, color, vine_id):
        self.desired_rfid = vine_id
        self.mqtt.publish(json.dumps({
            "event": "artifactUpdate",
            "id": self.id,
            "pendingRfid": vine_id,
            "color": color
        }))


