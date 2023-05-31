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
from printer.Result import Result
from printer.Boss import Boss
from printer.LeverInputController import LeverInputController
from logger.logger import Logger


# -----------------------------------------------------------------------
#   AdventureGenerator
#
#   Main class, use this to control the Explorey Printer.
# -----------------------------------------------------------------------
class AdventureGenerator(object):
    # 16, 18, 22, 32, 38, 40
    character_button_pin = 16
    encounter_button_pin = 18
    boss_button_pin = 22
    prize_button_pin = 32
    punishment_button_pin = 38
    duel_button_pin = 40

    print = True

    printer = None

    logger = None
    waiting_to_print = False

    levers = None

    character_count = 0
    encounter_count = 0

    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        self.logger = Logger()
        self.__init_pins()
        self.printer = AdventurePrinter()
        self.levers = LeverInputController(self.__levers_changed, self.logger)

    # Private -------------------------------------------

    def __init_pins(self):
        self.logger.log("Machine: initializing pins")

    def __character_button_cb(self, pin):
        self.logger.log(
            "Machine: character button pressed with waiting status: %s"
            % self.waiting_to_print
        )
        if self.waiting_to_print:
            self.logger.log("  Dispensing character")
            self.dispense_character()
            self.waiting_to_print = False
            t = threading.Timer(1.0, self.__allow_printing)
            t.start()

    def __encounter_button_cb(self, pin):
        self.logger.log(
            "Machine: encounter button pressed with waiting status: %s"
            % self.waiting_to_print
        )
        if self.waiting_to_print:
            self.logger.log("  Dispensing encounter")
            self.dispense_encounter()
            self.waiting_to_print = False
            t = threading.Timer(1.0, self.__allow_printing)
            t.start()

    def __prize_button_cb(self, pin):
        self.logger.log("Machine: prize button pressed")
        if self.waiting_to_print:
            self.logger.log("  Dispensing prize")
            self.dispense_prize()
            self.waiting_to_print = False
            t = threading.Timer(1.0, self.__allow_printing)
            t.start()

    def __punishment_button_cb(self, pin):
        self.logger.log("Machine: punishment button pressed")
        if self.waiting_to_print:
            self.logger.log("  Dispensing punishment")
            self.dispense_punishment()
            self.waiting_to_print = False
            t = threading.Timer(1.0, self.__allow_printing)
            t.start()

    def __boss_button_cb(self, pin):
        self.logger.log("Machine: boss button pressed")
        if self.waiting_to_print:
            self.logger.log("  Dispensing boss")
            self.dispense_boss()
            self.waiting_to_print = False
            t = threading.Timer(1.0, self.__allow_printing)
            t.start()

    def __duel_button_cb(self, pin):
        self.logger.log("Machine: duel button pressed")
        if self.waiting_to_print:
            self.logger.log("  Dispensing duel")
            self.dispense_duel()
            self.waiting_to_print = False
            t = threading.Timer(1.0, self.__allow_printing)
            t.start()

    def __allow_printing(self):
        self.waiting_to_print = True

    def __start_waiting_for_user(self):
        add_event_detection(
            self.character_button_pin, callback=self.__character_button_cb
        )
        add_event_detection(
            self.encounter_button_pin, callback=self.__encounter_button_cb
        )

        add_event_detection(self.prize_button_pin, callback=self.__prize_button_cb)
        add_event_detection(
            self.punishment_button_pin, callback=self.__punishment_button_cb
        )
        add_event_detection(self.boss_button_pin, callback=self.__boss_button_cb)
        add_event_detection(self.duel_button_pin, callback=self.__duel_button_cb)
        self.__allow_printing()

    def __levers_changed(self, levers):
        self.logger.log("Machine: levers changed to: %s" % levers)

    # Public --------------------------------------------
    def dispense_character(self):
        self.logger.log(
            "Machine: preparing to dispense character with printing set to: %s"
            % self.print
        )
        if self.print:
            character = CharacterSheet(levers=self.levers.currentValues)
            self.logger.log(character)
            self.character_count = self.character_count + 1
            self.printer.printCharacter(character)

    def dispense_encounter(self):
        self.logger.log(
            "Machine: preparing to dispense encounter with printing set to: %s"
            % self.print
        )
        if self.print:
            encounter = Encounter()
            self.logger.log(encounter)
            self.encounter_count = self.encounter_count + 1
            self.printer.printEncounter(encounter)

    def dispense_prize(self):
        self.logger.log(
            "Machine: preparing to dispense prize with printing set to: %s" % self.print
        )
        if self.print:
            result = Result(success=True)
            self.printer.printResult(result)

    def dispense_punishment(self):
        self.logger.log(
            "Machine: preparing to dispense punishment with printing set to: %s"
            % self.print
        )
        if self.print:
            result = Result(success=False)
            self.printer.printResult(result)

    def dispense_boss(self):
        self.logger.log(
            "Machine: preparing to dispense boss with printing set to: %s" % self.print
        )
        if self.print:
            boss = Boss()
            self.printer.printBoss(boss)

    def dispense_duel(self):
        self.logger.log(
            "Machine: preparing to dispense duel with printing set to: %s" % self.print
        )
        if self.print:
            self.logger.log("  Dispensing duel")
            # self.printer.printResult(result)

    def start(self):
        self.logger.log("Machine: starting")
        self.__start_waiting_for_user()

    def stop(self):
        self.logger.log("Machine: stopping")
        self.waiting_to_print = False
