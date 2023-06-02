from enum import IntEnum
import time
from lighting.PixelControl import PixelControl
from lighting.GenericButtonController import GenericButtonController
from lighting.Routine import *
from lighting.Colors import Colors
from lighting.DmxControl import DmxControl
import threading


NUM_PIXELS = 200

# Print
LILI_START = 21
LILI_END = 22
DANIELLE_START = 0
DANIELLE_END = 40
NAOMI_START = 23
NAOMI_END = 24
# War
DAVE_START = 0
DAVE_END = 50
TYLER_START = 50
TYLER_END = 100
# Beacon
BEACON_START = 120
BEACON_END = 200
STEM_START = 0
STEM_END = 120

ALL_PIXELS = range(0, NUM_PIXELS)

LILI_PIXELS = range(LILI_START, LILI_END)
DANIELLE_PIXELS = range(DANIELLE_START, DANIELLE_END)
NAOMI_PIXELS = range(NAOMI_START, NAOMI_END)
DAVE_PIXELS = range(DAVE_START, DAVE_END)
TYLER_PIXELS = range(TYLER_START, TYLER_END)
BEACON_PIXELS = range(BEACON_START, BEACON_END)
STEM_PIXELS = range(STEM_START, STEM_END)

WAR_ROUTINE_INDEX = 0

MODE_PRINT = 0
MODE_WAR = 1
MODE_BEACON = 2


class ExploreyLights(object):
    pixels = None
    thread = None
    dmx = DmxControl()
    mode = 0
    delay = 0.01
    num_pixels = 0
    dmxBlackLights = [17, 10]
    now = 0

    def __init__(self, mode=MODE_PRINT):
        self.mode = mode
        if mode is MODE_PRINT:
            self.num_pixels = 50
        elif mode is MODE_WAR:
            self.num_pixels = 100
        else:
            self.num_pixels = 200

        self.pixels = PixelControl(self.num_pixels)
        self.mode_object = None
        self.setup_mode()

    # ------------------------------ Cave Black lights ----------------------------------------

    blackLightValue = 0
    blackLightUp = True
    blackLightWait = False
    blackLightDuration = 2000
    blackLightTimestamp = 0
    blackLightRunning = False

    def processBlackLights(self):
        if not self.blackLightRunning:
            self.blackLightRunning = True
            self.blackLightUp = True
            self.blackLightTimestamp = self.now
            self.blackLightDuration = random.randrange(500, 2000)
        finish_time = self.blackLightTimestamp + self.blackLightDuration
        if self.blackLightWait:
            if self.now > finish_time:
                self.blackLightWait = False
                self.blackLightTimestamp = self.now
                self.blackLightUp = not self.blackLightUp
                self.blackLightDuration = random.randrange(500, 5000)
        elif self.blackLightUp:
            if self.now > finish_time:
                self.blackLightWait = True
                self.blackLightDuration = random.randrange(1000, 8000)
                self.blackLightTimestamp = self.now

            amount_left = 1.0 - (
                (float(finish_time) - float(self.now)) / float(self.blackLightDuration)
            )
            self.blackLightValue = int(round(amount_left * 100.0))
            self.dmx.setBlackLight(self.dmxBlackLights[0], self.blackLightValue)
            self.dmx.setBlackLight(self.dmxBlackLights[1], self.blackLightValue)
        else:
            if self.now > finish_time:
                self.blackLightWait = True
                self.blackLightDuration = random.randrange(10000, 30000)
            amount_left = (float(finish_time) - float(self.now)) / float(
                self.blackLightDuration
            )
            self.blackLightValue = int(round(amount_left * 100.0))
            self.dmx.setBlackLight(self.dmxBlackLights[0], self.blackLightValue)
            self.dmx.setBlackLight(self.dmxBlackLights[1], self.blackLightValue)

    # ------------------------------ END Cave Black Light -------------------------------------

    def setup_mode(self):
        if self.mode is MODE_PRINT:
            self.mode_object = MultiRoutine(
                [
                    # CyclingMultiRoutine(
                    #     [
                    #         [
                    #             WaveRoutine(
                    #                 self.pixels,
                    #                 NAOMI_PIXELS,
                    #                 [
                    #                     Colors.mid_green,
                    #                     Colors.mixed_blue,
                    #                     Colors.light_green,
                    #                     Colors.red,
                    #                 ],
                    #                 wave_wait_time=5000,
                    #             ),
                    #             30000,
                    #         ],
                    #         [RainbowRoutine(self.pixels, NAOMI_PIXELS), 5000],
                    #         [
                    #             WaveRoutine(
                    #                 self.pixels,
                    #                 NAOMI_PIXELS,
                    #                 [
                    #                     Colors.mixed_blue,
                    #                     Colors.light_green,
                    #                     Colors.mid_green,
                    #                     Colors.red,
                    #                 ],
                    #                 wave_wait_time=3000,
                    #             ),
                    #             30000,
                    #         ],
                    #         [
                    #             WaveRoutine(
                    #                 self.pixels,
                    #                 NAOMI_PIXELS,
                    #                 [
                    #                     Colors.mid_green,
                    #                     Colors.mixed_blue,
                    #                     Colors.light_green,
                    #                     Colors.red,
                    #                 ],
                    #                 wave_wait_time=5000,
                    #             ),
                    #             30000,
                    #         ],
                    #         [FireRoutine(self.pixels, NAOMI_PIXELS), 20000],
                    #         [
                    #             PulseRoutine(
                    #                 self.pixels, NAOMI_PIXELS, Colors.mid_green
                    #             ),
                    #             5000,
                    #         ],
                    #     ]
                    # ),
                    MushroomRoutine(self.pixels, DANIELLE_PIXELS),
                    # WaveRoutine(
                    #     self.pixels,
                    #     LILI_PIXELS,
                    #     [
                    #         Colors.mixed_blue,
                    #         Colors.light_green,
                    #         Colors.mid_green,
                    #         Colors.red,
                    #     ],
                    # ),
                    #             WaveRoutine(self.pixels, ALL_PIXELS, [Colors.mid_green, Colors.mixed_blue, Colors.light_green, Colors.red], delay=1000),
                ]
            )
        elif self.mode is MODE_WAR:
            self.mode_object = MultiRoutine(
                [
                    FireRoutine(self.pixels, DAVE_PIXELS),
                    BleuRoutine(self.pixels, TYLER_PIXELS),
                    #             WaveRoutine(self.pixels, ALL_PIXELS, [Colors.mid_green, Colors.mixed_blue, Colors.light_green, Colors.red], delay=1000),
                ]
            )
        else:
            self.mode_object = MultiRoutine(
                [
                    PulseRoutine(self.pixels, BEACON_PIXELS, Colors.mid_green),
                    WaveRoutine(self.pixels, STEM_PIXELS, [Colors.yellow]),
                ]
            )

    def update_war_routine(self, routine):
        if self.mode is MODE_WAR:
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
            middle_index = len(FRONT_MID) // 2
            reverse_FRONT_LEFT = FRONT_LEFT[:]
            reverse_FRONT_LEFT.reverse()
            reverse_FRONT_LEFT_MID = FRONT_LEFT_MID[:]
            reverse_FRONT_LEFT_MID.reverse()
            reverse_left_FRONT_MID = FRONT_MID[middle_index:]
            reverse_left_FRONT_MID.reverse()
            self.mode_object = MultiRoutine(
                [
                    RainbowRoutine(self.pixels, BAR_TOP_PIXELS),
                    RainbowRoutine(self.pixels, BAR_BOTTOM_PIXELS),
                    WaveRoutine(
                        self.pixels,
                        reverse_FRONT_LEFT,
                        [
                            Colors.mid_green,
                            Colors.mixed_blue,
                            Colors.light_green,
                            Colors.red,
                        ],
                        delay=1000,
                    ),
                    WaveRoutine(
                        self.pixels,
                        reverse_FRONT_LEFT_MID,
                        [
                            Colors.light_green,
                            Colors.mid_green,
                            Colors.mixed_blue,
                            Colors.red,
                        ],
                        delay=4000,
                    ),
                    WaveRoutine(
                        self.pixels,
                        reverse_left_FRONT_MID,
                        [
                            Colors.mixed_blue,
                            Colors.light_green,
                            Colors.mid_green,
                            Colors.red,
                        ],
                    ),
                    WaveRoutine(
                        self.pixels,
                        FRONT_MID[:middle_index],
                        [
                            Colors.mixed_blue,
                            Colors.mid_green,
                            Colors.light_green,
                            Colors.red,
                        ],
                    ),
                    WaveRoutine(
                        self.pixels,
                        FRONT_RIGHT_MID,
                        [
                            Colors.light_green,
                            Colors.mid_green,
                            Colors.mixed_blue,
                            Colors.red,
                        ],
                        delay=4000,
                    ),
                    WaveRoutine(
                        self.pixels,
                        FRONT_RIGHT,
                        [
                            Colors.mid_green,
                            Colors.mixed_blue,
                            Colors.light_green,
                            Colors.red,
                        ],
                        delay=1000,
                    ),
                ]
            )
        else:
            self.mode_object = None

    def set_pixels(self, indexes, color):
        for i in indexes:
            self.pixels.setRGBW(i, color)
        self.pixels.render()

    def __run_thread(self):
        while self.is_running:
            self.now = int(round(time.time() * 1000))
            self.mode_object.tick()
            self.pixels.render()
            self.processBlackLights()
            self.dmx.render()
            # self.dmx.render()
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
