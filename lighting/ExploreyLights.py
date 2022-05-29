from enum import IntEnum
import time
from lighting.PixelControl import PixelControl
from lighting.GenericButtonController import GenericButtonController
from lighting.Routine import *
from lighting.Colors import Colors
import threading


NUM_PIXELS = 50

LILI_START = 10
LILI_END = 18
DANIELLE_START = 18
DANIELLE_END = 30
NAOMI_START = 0
NAOMI_END = 10
DAVE_START = 0
DAVE_END = 25
TYLER_START = 26
TYLER_END = 50

ALL_PIXELS = range(0, NUM_PIXELS)

LILI_PIXELS = range(LILI_START, LILI_END)
DANIELLE_PIXELS = range(DANIELLE_START, DANIELLE_END)
NAOMI_PIXELS = range(NAOMI_START, NAOMI_END)
DAVE_PIXELS = range(DAVE_START, DAVE_END)
TYLER_PIXELS = range(TYLER_START, TYLER_END)

WAR_ROUTINE_INDEX = 0

class ExploreyLights(object):
    pixels = None
    thread = None
    mode = 0
    delay = 0.01
    is_print_machine = None

    def __init__(self, is_print_machine=True):
        self.is_print_machine = is_print_machine
        self.pixels = PixelControl(NUM_PIXELS)
        self.mode_object = None
        self.setup_mode()

    def setup_mode(self):
#         if is_print_machine:
#             self.mode_object = MultiRoutine([
#                 CyclingMultiRoutine([
#                     [
#                         WaveRoutine(self.pixels, NAOMI_PIXELS, [Colors.mid_green, Colors.mixed_blue, Colors.light_green, Colors.red], wave_wait_time=5000),
#                         30000
#                     ],
#                     [
#                         RainbowRoutine(self.pixels, NAOMI_PIXELS),
#                         5000
#                     ],
#                     [
#                         WaveRoutine(self.pixels, NAOMI_PIXELS, [Colors.mixed_blue, Colors.light_green, Colors.mid_green, Colors.red], wave_wait_time=3000),
#                         30000
#                     ],
#                     [
#                         WaveRoutine(self.pixels, NAOMI_PIXELS, [Colors.mid_green, Colors.mixed_blue, Colors.light_green, Colors.red], wave_wait_time=5000),
#                         30000
#                     ],
#                     [
#                         FireRoutine(self.pixels, NAOMI_PIXELS),
#                         20000
#                     ],
#                     [
#                         PulseRoutine(self.pixels, NAOMI_PIXELS, Colors.mid_green),
#                         5000
#                     ],
#                 ]),
#                 BleuRoutine(self.pixels, DANIELLE_PIXELS),
#                 WaveRoutine(self.pixels, LILI_PIXELS, [Colors.mixed_blue, Colors.light_green, Colors.mid_green, Colors.red]),
#     #             WaveRoutine(self.pixels, ALL_PIXELS, [Colors.mid_green, Colors.mixed_blue, Colors.light_green, Colors.red], delay=1000),
#             ])
#         else:
        self.mode_object = MultiRoutine([
            FireRoutine(self.pixels, DAVE_PIXELS),
#                 BleuRoutine(self.pixels, TYLER_PIXELS),
#             WaveRoutine(self.pixels, ALL_PIXELS, [Colors.mid_green, Colors.mixed_blue, Colors.light_green, Colors.red], delay=1000),
        ])

    def update_war_routine(self, routine):
        if not self.is_print_machine:
            self.mode_object.routines[WAR_ROUTINE_INDEX] = routine

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
            self.mode_object.tick()
            self.pixels.render()
            time.sleep(self.delay)

    def start(self):
        self.thread = threading.Thread(target=self.__run_thread)
        self.is_running = True
        self.thread.start()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.thread.join()
            self.thread = None
            self.pixels.blackout()
            self.pixels.render()

