import json

from lighting.Colors import Colors
from lighting.routines import Routines

CARD_FOUND = "cardFound"
CARD_REMOVED = "cardRemoved"
FINISHED_BOOT = "finishedBoot"


ARTIFACT_CITY = "artifact/city"
ARTIFACT_TANK = "artifact/tank"
ARTIFACT_MICROWAVE = "artifact/microwave"
ARTIFACT_BUGS = "artifact/bugs"
ARTIFACT_FISH = "artifact/fish"
ARTIFACT_MUSHROOMS = "artifact/mushrooms"
ARTIFACT_VOLCANO = "artifact/volcano"
ARTIFACT_MOBILE = "artifact/mobile"


class Artifact(object):
    id = None
    mqtt = None
    color = None
    current_rfid = None
    desired_rfid = None
    on_change = None

    def __init__(self, mqtt, artifact_id, on_change):
        self.mqtt = mqtt
        self.id = artifact_id
        self.on_change = on_change

        self.mqtt.listen(self.__parse_mqtt_event)
        self.reset()

    def __parse_mqtt_event(self, event):
        try:
            events = json.loads(event)
            if not type(events) in (tuple, list):
                events = [events]
            for data in events:
                if data and data["event"]:
                    event = data["event"]
                    if event == CARD_FOUND or event == CARD_REMOVED or event == FINISHED_BOOT:
                        reader_name = data["reader"]
                        if reader_name == self.id:
                            if event == CARD_FOUND:
                                card_id = data["card"]
                                self.__on_card_detected(card_id)
                            elif event == CARD_REMOVED:
                                previous_card = data["previousCard"]
                                self.__on_card_removed(previous_card)
                            elif event == FINISHED_BOOT:
                                self.set_pending_vine(self.color, self.desired_rfid)
        except Exception as e:
            print("Artifact Failed parsing event", event, e)

    def __on_card_detected(self, card):
        print("Card detected", card)
        self.current_rfid = card
        self.on_change(self, True, card)

    def __on_card_removed(self, previous_card):
        print("card removed")
        self.current_rfid = None
        self.is_attached = False
        self.on_change(self, False, previous_card)

    def _send_update(self, start_time=-1, end_time=-1, should_disconnect=True):
        color = self.color
        if color is None:
            color = 0
        self.mqtt.queue_in_batch_publish({
            "event": "artifactUpdate",
            "reader": self.id,
            "id": self.id,
            "pendingRfid": self.desired_rfid,
            "color": color,
            "startTime": start_time,
            "endTime": end_time,
            "shouldDisconnect": should_disconnect
        })

    def reset(self):
        self.color = None
        self.desired_rfid = None
        self._send_update()

    def set_pending_vine(self, color, rfid):
        self.color = color
        self.desired_rfid = rfid
        self._send_update()



