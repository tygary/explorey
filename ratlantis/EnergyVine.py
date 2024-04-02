from lighting.Colors import Colors
from lighting.routines import Routines
from ratlantis.Electromagnet import Electromagnet


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
        print("pulsing color", self.light_addresses)
        self.light_routine = Routines.PulseRoutine(self.pixels, self.light_addresses, Colors.mid_green)  # Routines.FireRoutine(self.pixels, self.light_addresses, color_index)

    def wave(self, color):
        self.light_routine = Routines.BleuRoutine(self.pixels, self.light_addresses)
        # Routines.WaveRoutine(self.pixels, self.light_addresses, [color])

    def stop(self):
        self.light_routine = Routines.BlackoutRoutine(self.pixels, self.light_addresses)

    def update(self):
        self.light_routine.tick()
        self.magnet.update()

    def detach(self):
        print("Detaching")
        self.magnet.turn_off()
