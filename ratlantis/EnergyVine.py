from Electromagnet import Electromagnet
from lighting.Routine import *


class EnergyVine(object):
    rfid = None
    magnet = None
    light_addresses = None
    pixels = None
    light_routine = None

    def __init__(self, rfid, magnet_pin, light_addresses, pixels):
        self.rfid = rfid
        self.magnet = Electromagnet(magnet_pin)
        self.light_addresses = light_addresses
        self.pixels = pixels
        self.stop()

    def pulse_color(self, color_index):
        self.light_routine = FireRoutine(self.pixels, self.light_addresses, color_index)

    def wave(self, color):
        self.light_routine = WaveRoutine(self.pixels, self.light_addresses, [color])

    def stop(self):
        self.light_routine = BlackoutRoutine(self.pixels, self.light_addresses)

    def update(self):
        self.light_routine.tick()
        self.magnet.update()

    def detach(self):
        self.magnet.turn_off()
