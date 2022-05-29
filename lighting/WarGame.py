from lighting.GenericButtonController import GenericButtonController
from lighting.ExploreyLights import *

MAX_POINTS = 1000

RED_BUTTON_PIN = 18
BLUE_BUTTON_PIN = 22

class WarGame(object):
    pixels = None
    explorey_lights = None
    points = 0
    pixel_start = 0
    pixel_end = 0
    num_pixels = 0

    buttons = None

    def __init__(self, pixels, explorey_lights):
        self.explorey_lights = explorey_lights
        self.pixel_start = DAVE_START
        self.pixel_end = DAVE_END
        self.num_pixels = DAVE_END - DAVE_START

        self.buttons = GenericButtonController()

        self.buttons.add_event_detection(RED_BUTTON_PIN, self.on_red_button)
        self.buttons.add_event_detection(BLUE_BUTTON_PIN, self.on_blue_button)

    def on_red_button(self):
        if self.points < MAX_POINTS:
            self.points += 1
        self.render()

    def on_blue_button(self):
        if (self.points > (MAX_POINTS * -1)):
            self.points -= 1
        self.render()

    def render(self):

        perc_lost = self.points + MAX_POINTS / (MAX_POINTS * 2)

        middle_pixel = round(perc_lost * self.num_pixels)


        routine = MultiRoutine([
            WaveRoutine(self.explorey_lights.pixels, range(self.pixel_start, middle_pixel), [Colors.red]),
            RainbowRoutine(self.explorey_lights.pixels, [middle_pixel]),
            WaveRoutine(self.explorey_lights.pixels, range(middle_pixel + 1, self.pixel_end), [Colors.mixed_blue, Colors.yellow]),
        ])
        self.explorey_lights.update_war_routine(routine)


		


