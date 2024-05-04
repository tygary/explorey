from lighting.Colors import Colors
from lighting.routines import Routines

COLOR_RED = 0
COLOR_ORANGE = 0.07
COLOR_YELLOW = 0.22
COLOR_GREEN = 0.47
COLOR_LIGHT_BLUE = 0.59
COLOR_BLUE = 0.72
COLOR_PURPLE = 0.88
COLOR_PINK = 1
COLORS = [COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_LIGHT_BLUE, COLOR_BLUE, COLOR_PURPLE, COLOR_PINK]


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
    light_routine = None

    def __init__(self, rfid, light_addresses, pixels):
        self.rfid = rfid
        self.light_addresses = light_addresses
        self.pixels = pixels
        self.off()

    def invalid_connection(self):
        print("invalid connection!", self.light_addresses)
        self.light_routine = Routines.FireRoutine(self.pixels, self.light_addresses)

    def valid_connection(self, color):
        self.light_routine = Routines.WaveRoutine(
            self.pixels,
            self.light_addresses,
            get_color(color),  # [Colors.light_green, Colors.mid_green, Colors.green],
            wave_wait_time=1000
        )

    def pending_connection(self, color):
        print("pulsing color", self.light_addresses)
        self.light_routine = Routines.PulseRoutine(self.pixels, self.light_addresses, get_color(color))  # Colors.mid_green

    def off(self):
        self.light_routine = Routines.BlackoutRoutine(self.pixels, self.light_addresses)

    def update(self):
        self.light_routine.tick()
