import RPi.GPIO as GPIO
import threading

from printer.addeventdetection import *
from logger.logger import Logger
from sound.MusicControlSystem import MusicControlSystem


class BatJourney(object):
    start_button_pin = 18
    stop_button_pin = 22

    music = None

    allow_input = False

    logger = None

    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        self.logger = Logger()
        self.__init_pins()
        self.music = MusicControlSystem()


    # Private -------------------------------------------

    def __init_pins(self):
        self.logger.log("Machine: initializing pins")

    def __start_button_cb(self, pin):
        self.logger.log("Machine: fact button pressed with waiting status: %s" % self.waiting_to_print)
        if self.allow_input == True:
            self.logger.log("  Starting journey")
            self.music.play_bat_journey()
            self.allow_input = False
            t = threading.Timer(1.0, self.__allow_input)
            t.start()

    def __stop_button_cb(self, pin):
        self.logger.log("Machine: stop button pressed with waiting status: %s" % self.waiting_to_print)
        if self.allow_input == True:
            self.logger.log("  Stopping Journey")
            self.music.player.stop_music()
            self.allow_input = False
            t = threading.Timer(1.0, self.__allow_input)
            t.start()

    def __allow_input(self):
        self.allow_input = True

    def __start_waiting_for_user(self):
        self.logger.log("Machine: waiting for user at pins %s and %s" % (self.start_button_pin, self.stop_button_pin))
        add_event_detection(self.start_button_pin, callback=self.__start_button_cb)
        add_event_detection(self.stop_button_pin, callback=self.__stop_button_cb)
        self.__allow_input()


    # Public --------------------------------------------

    def start(self):
        self.logger.log("Bat Journey: startup")
        self.__start_waiting_for_user()

    def stop(self):
        self.logger.log("Bat Journey: shutdown")
        self.allow_input = False
