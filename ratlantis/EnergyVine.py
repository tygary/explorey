import json
import random

from lighting.Colors import Colors
from lighting.routines import Routines

COLOR_RED = 0.01
COLOR_ORANGE = 0.07
COLOR_YELLOW = 0.22
COLOR_GREEN = 0.47
COLOR_LIGHT_BLUE = 0.59
COLOR_BLUE = 0.72
COLOR_PURPLE = 0.88
COLOR_PINK = 1
COLORS = [COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_LIGHT_BLUE, COLOR_BLUE, COLOR_PURPLE, COLOR_PINK]

EVENT_VINE_UPDATE = "vineUpdate"
VINE_MODE_CONNECTED = 0
VINE_MODE_INVALID = 1
VINE_MODE_PENDING = 2
VINE_MODE_OFF = 3

VINE_ONE_RFID = "f1011466080104e0"
VINE_TWO_RFID = "2dcc1366080104e0"
VINE_THREE_RFID = "7DC70A09530104E0"
VINE_FOUR_RFID = "7DC70A09530104E0"
VINE_FIVE_RFID = "2ccc1366080104e0"
VINE_SIX_RFID = "7fec1366080104e0"
VINE_SEVEN_RFID = "9fd81366080104e0"
VINE_EIGHT_RFID = "b8f61366080104e0"


def get_color(color_const):
    if color_const == COLOR_RED:
        return Colors.red
    if color_const == COLOR_ORANGE:
        return Colors.orange
    if color_const == COLOR_YELLOW:
        return Colors.yellow
    if color_const == COLOR_GREEN:
        return Colors.light_green
    if color_const == COLOR_LIGHT_BLUE:
        return Colors.soft_blue
    if color_const == COLOR_BLUE:
        return Colors.blue
    if color_const == COLOR_PURPLE:
        return Colors.purple
    else:  # if color_const == COLOR_PINK:
        return Colors.pink


class EnergyVine(object):
    rfid = None
    light_addresses = None
    pixels = None
    mqtt = None
    light_routine = None
    color = None

    def __init__(self, rfid, light_addresses, pixels, mqtt):
        self.rfid = rfid
        self.light_addresses = light_addresses
        self.pixels = pixels
        self.mqtt = mqtt
        self.off()
        self.mqtt.listen(self.__parse_mqtt_event)

    def __parse_mqtt_event(self, event):
        try:
            events = json.loads(event)
            if not type(events) in (tuple, list):
                events = [events]
            for data in events:
                if data and data["event"] and data["event"] == EVENT_VINE_UPDATE:
                    rfid = data["rfid"]
                    mode = data["mode"]
                    color = data["color"]
                    if rfid == self.rfid:
                        if mode == VINE_MODE_CONNECTED:
                            self.valid_connection(color)
                        elif mode == VINE_MODE_INVALID:
                            self.invalid_connection()
                        elif mode == VINE_MODE_PENDING:
                            self.pending_connection(color)
                        elif mode == VINE_MODE_OFF:
                            self.off()
        except Exception as e:
            print("Energy Vine Failed parsing event", event, e)

    def invalid_connection(self):
        print("invalid connection!", self.light_addresses)
        self.light_routine = Routines.FireRoutine(self.pixels, self.light_addresses)

    def valid_connection(self, color):
        self.color = color
        self.light_routine = Routines.FireRoutine(
            self.pixels,
            self.light_addresses,
            [get_color(color)]  # [Colors.light_green, Colors.mid_green, Colors.green],
        )

    def pending_connection(self, color):
        if color == -1:
            print(self.rfid, "party mode", color)
            non_green_colors = [
                Colors.red,
                Colors.pink,
                Colors.purple,
                Colors.orange,
                Colors.yellow,
                Colors.mid_green,
                Colors.light_green,
                Colors.soft_blue,
                Colors.mixed_blue
            ]
            self.light_routine = Routines.WaveRoutine(self.pixels, self.light_addresses, [random.choice(non_green_colors)])  # Colors.mid_green
        else:
            self.color = color
            print(self.rfid, "pulsing color", color)
            self.light_routine = Routines.PulseRoutine(self.pixels, self.light_addresses, get_color(color))  # Colors.mid_green

    def off(self):
        self.color = None
        print(self.rfid, "is off")
        self.light_routine = Routines.BlackoutRoutine(self.pixels, self.light_addresses)

    def update(self):
        self.light_routine.tick()


class RemoteEnergyVine(object):
    rfid = None
    mqtt = None
    color = None
    mode = VINE_MODE_OFF

    def __init__(self, rfid, mqtt):
        self.rfid = rfid
        self.mqtt = mqtt
        self._send_update()

    def _send_update(self):
        print("Vine", self.rfid, "mode", self.mode, "color", self.color)
        self.mqtt.queue_in_batch_publish({
            "event": EVENT_VINE_UPDATE,
            "mode": self.mode,
            "rfid": self.rfid,
            "color": self.color,
            "shouldDisconnect": True
        })

    def invalid_connection(self):
        if self.mode != VINE_MODE_CONNECTED:
            # self.color = None
            self.mode = VINE_MODE_INVALID
            self._send_update()

    def valid_connection(self, color):
        if self.mode != VINE_MODE_CONNECTED or self.color != color:
            self.color = color
            self.mode = VINE_MODE_CONNECTED
            self._send_update()

    def pending_connection(self, color):
        if self.mode != VINE_MODE_PENDING or self.color != color:
            self.color = color
            self.mode = VINE_MODE_PENDING
            self._send_update()

    def off(self):
        if self.mode != VINE_MODE_OFF:
            self.color = None
            self.mode = VINE_MODE_OFF
            self._send_update()

