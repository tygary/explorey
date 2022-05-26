from enum import IntEnum
import time
from lighting.PixelControl import PixelControl
from lighting.GenericButtonController import GenericButtonController
from lighting.Routine import *
from lighting.Colors import Colors
import threading


NUM_PIXELS = 50

MODE_ON = 0
MODE_COLOR = 1
MODE_RAINBOW = 2
MODE_FIRE = 3
MODE_WAVE = 4
NUM_MODES = 5

ALL_PIXELS = range(0, 50)

# BAR_TOP_PIXELS = range(51, 149)

class ExploreyLights(object):
    pixels = None
    thread = None
    mode = 0

    def __init__(self):
        self.pixels = PixelControl(NUM_PIXELS)
        self.mode_object = None
        self.setup_mode()

    def setup_mode(self):
        self.mode_object = MultiRoutine([
            RainbowRoutine(self.pixels, ALL_PIXELS),
        ])

    def change_mode(self):
        self.mode = (self.mode + 1) % NUM_MODES
        print("New Mode - {}".format(self.mode))
        if self.mode is MODE_COLOR:
            self.mode_object = PulseRoutine(self.pixels, FRONT_PIXELS, Colors.mid_green)
        elif self.mode is MODE_RAINBOW:
            self.mode_object = RainbowRoutine(self.pixels, ALL_PIXELS)
        elif self.mode is MODE_FIRE:
            self.mode_object = FireRoutine(self.pixels, ALL_PIXELS)
        elif self.mode is MODE_WAVE:
            middle_index = len(FRONT_MID)//2
            reverse_FRONT_LEFT = FRONT_LEFT[:]
            reverse_FRONT_LEFT.reverse()
            reverse_FRONT_LEFT_MID = FRONT_LEFT_MID[:]
            reverse_FRONT_LEFT_MID.reverse()
            reverse_left_FRONT_MID = FRONT_MID[middle_index:]
            reverse_left_FRONT_MID.reverse()
            self.mode_object = MultiRoutine([
                RainbowRoutine(self.pixels, BAR_TOP_PIXELS),
                RainbowRoutine(self.pixels, BAR_BOTTOM_PIXELS),
                WaveRoutine(self.pixels, reverse_FRONT_LEFT, [Colors.mid_green, Colors.mixed_blue, Colors.light_green, Colors.red], delay=1000),
                WaveRoutine(self.pixels, reverse_FRONT_LEFT_MID, [Colors.light_green, Colors.mid_green, Colors.mixed_blue, Colors.red], delay=4000),
                WaveRoutine(self.pixels, reverse_left_FRONT_MID, [Colors.mixed_blue, Colors.light_green, Colors.mid_green, Colors.red]),
                WaveRoutine(self.pixels, FRONT_MID[:middle_index], [Colors.mixed_blue, Colors.mid_green, Colors.light_green, Colors.red]),
                WaveRoutine(self.pixels, FRONT_RIGHT_MID, [Colors.light_green, Colors.mid_green, Colors.mixed_blue, Colors.red], delay=4000),
                WaveRoutine(self.pixels, FRONT_RIGHT, [Colors.mid_green, Colors.mixed_blue, Colors.light_green, Colors.red], delay=1000)
            ])
        else:
            self.mode_object = None

    def set_pixels(self, indexes, color):
        for i in indexes:
            self.pixels.setRGBW(i, color)
        self.pixels.render()

    def __run_thread(self):
        while self.is_running:
            self.pixels.render()

    def start(self):
        self.thread = threading.Thread(target=self.__run_thread)
        self.is_running = True
        self.thread.start()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.thread.join()
            self.thread = None

