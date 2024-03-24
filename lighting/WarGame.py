from lighting.GenericButtonController import GenericButtonController
from lighting.ExploreyLights import *
from lighting.routines.Routine import Routines

MAX_POINTS = 1000

RED_BUTTON_PIN = 18
BLUE_BUTTON_PIN = 22

class WarGame(object):
    explorey_lights = None
    points = 0
    pixel_start = 0
    pixel_end = 0
    num_pixels = 0

    advance_duration = 1000
    next_advance = 0

    thread = None
    is_running = False

    buttons = None
    delay = 0.25

    prev_middle_pixel = 0

    def __init__(self, explorey_lights):
        self.explorey_lights = explorey_lights
        self.pixel_start = DAVE_START
        self.pixel_end = DAVE_END
        self.num_pixels = DAVE_END - DAVE_START

        self.buttons = GenericButtonController()

        self.buttons.add_event_detection(RED_BUTTON_PIN, self.on_red_button)
        self.buttons.add_event_detection(BLUE_BUTTON_PIN, self.on_blue_button)

    def on_red_button(self, pin):
        if (self.points > (MAX_POINTS * -1)):
            self.points += 1
            print("Red button: %s" % self.points)
        else:
            print("YOU WIN!")
        self.render()

    def on_blue_button(self, pin):
        if (self.points > (MAX_POINTS * -1)):
            self.points += 10
            print("Blue button: %s" % self.points)
        else:
            print("YOU WIN!")
        self.render()

    def __advance_thread(self):
        while self.is_running:
            now = int(round(time.time() * 1000))
            if now > self.next_advance and self.points < MAX_POINTS:
                self.points += 30
                print("Advancing...")
                self.next_advance = now + self.advance_duration
                self.render()
            time.sleep(self.delay)


    def render(self):
        perc_lost = (self.points + MAX_POINTS) / (MAX_POINTS * 2)

        middle_pixel = round(perc_lost * self.num_pixels)

        if (middle_pixel != self.prev_middle_pixel):
            routine = Routines.MultiRoutine([
                Routines.WaveRoutine(self.explorey_lights.pixels, range(self.pixel_start, middle_pixel), [Colors.red], wave_wait_time=2000),
    #             Routines.PulseRoutine(self.explorey_lights.pixels, range(self.pixel_start, middle_pixel), Colors.red),
                Routines.RainbowRoutine(self.explorey_lights.pixels, [middle_pixel]),
                Routines.WaveRoutine(self.explorey_lights.pixels, range(middle_pixel + 1, self.pixel_end), [Colors.mixed_blue, Colors.yellow], wave_wait_time=2000),
    #             Routines.PulseRoutine(self.explorey_lights.pixels, range(middle_pixel + 1, self.pixel_end), Colors.mixed_blue),
            ])
            self.explorey_lights.update_war_routine(routine)
            self.prev_middle_pixel = middle_pixel

    def start(self):
        self.thread = threading.Thread(target=self.__advance_thread)
        self.is_running = True
        self.thread.start()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.thread.join()
            self.thread = None

