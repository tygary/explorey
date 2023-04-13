import RPi.GPIO as GPIO
import time
import threading
import imp
import random
import textwrap
from printer.AdventurePrinter import AdventurePrinter
from printer.addeventdetection import *
from printer.CharacterSheet import CharacterSheet
from printer.Encounter import Encounter
from logger.logger import Logger


# -----------------------------------------------------------------------
#   AdventureGenerator
#
#   Main class, use this to control the Explorey Printer.
# -----------------------------------------------------------------------
class AdventureGenerator(object):
    character_button_pin = 18
    encounter_button_pin = 22

    print = True

    printer = None

    logger = None
    waiting_to_print = False

    character_count = 0
    encounter_count = 0

    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        self.logger = Logger()
        self.__init_pins()
        self.printer = AdventurePrinter()

    # Private -------------------------------------------

    def __init_pins(self):
        self.logger.log("Machine: initializing pins")

    def __character_button_cb(self, pin):
        self.logger.log("Machine: character button pressed with waiting status: %s" % self.waiting_to_print)
        if self.waiting_to_print:
            self.logger.log("  Dispensing character")
            self.dispense_character()
            self.waiting_to_print = False
            t = threading.Timer(1.0, self.__allow_printing)
            t.start()

    def __encounter_button_cb(self, pin):
        self.logger.log("Machine: encounter button pressed with waiting status: %s" % self.waiting_to_print)
        if self.waiting_to_print:
            self.logger.log("  Dispensing encounter")
            self.dispense_encounter()
            self.waiting_to_print = False
            t = threading.Timer(1.0, self.__allow_printing)
            t.start()

    def __allow_printing(self):
        self.waiting_to_print = True

    def __start_waiting_for_user(self):
        self.logger.log("Machine: waiting for user at pins %s and %s" % (self.character_button_pin, self.encounter_button_pin))
        add_event_detection(self.character_button_pin, callback=self.__character_button_cb)
        add_event_detection(self.encounter_button_pin, callback=self.__encounter_button_cb)
        self.__allow_printing()

    # Public --------------------------------------------
    def dispense_character(self):
        self.logger.log("Machine: preparing to dispense character with printing set to: %s" % self.print_facts)
        if self.print:
            character = CharacterSheet()
            self.logger.log(character)
            self.character_count = self.character_count + 1
            self.printer.printCharacter(character)

    def dispense_encounter(self):
        self.logger.log("Machine: preparing to dispense encounter with printing set to: %s" % self.print_facts)
        if self.print:
            encounter = Encounter()
            self.logger.log(encounter)
            self.encounter_count = self.encounter_count + 1
            self.printer.printEncounter(encounter)

    def start(self):
        self.logger.log("Machine: starting")
        self.__start_waiting_for_user()

    def stop(self):
        self.logger.log("Machine: stopping")
        self.waiting_to_print = False
