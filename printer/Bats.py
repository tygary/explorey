import RPi.GPIO as GPIO
import time
import threading
import imp
import random
import textwrap
from printer.printer import Printer
from printer.addeventdetection import *
from logger.logger import Logger

##-----------------------------------------------------------------------
#   Vending Machine
#
#   Main class, use this to control the Explorey Printer.
##-----------------------------------------------------------------------
class Bats(object):
    fact_button_pin = 18
    badge_button_pin = 22

    print_facts = True

    printer = None

    logger = None

    fact_count = 0
    badge_count = 0

    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        self.logger = Logger()
        self.__init_pins()
        self.printer = Printer()

    # Private -------------------------------------------

    def __init_pins(self):
        self.logger.log("Machine: initializing pins")

    def __fact_button_cb(self, pin):
        self.logger.log("Machine: fact button pressed with waiting status: %s" % self.waiting_to_print)
        if self.waiting_to_print == True:
            self.logger.log("  Dispensing fact")
            self.dispense_fact()
            self.waiting_to_print = False
            t = threading.Timer(1.0, self.__allow_printing)
            t.start()

    def __badge_button_cb(self, pin):
        self.logger.log("Machine: badge button pressed with waiting status: %s" % self.waiting_to_print)
        if self.waiting_to_print == True:
            self.logger.log("  Dispensing Badge")
            self.dispense_badge()
            self.waiting_to_print = False
            t = threading.Timer(1.0, self.__allow_printing)
            t.start()

    def __allow_printing(self):
        self.waiting_to_print = True

    def __start_waiting_for_user(self):
        self.logger.log("Machine: waiting for user at pins %s and %s" % (self.fact_button_pin, self.badge_button_pin))
        add_event_detection(self.fact_button_pin, callback=self.__fact_button_cb)
        add_event_detection(self.badge_button_pin, callback=self.__badge_button_cb)
        self.__allow_printing()


    # Public --------------------------------------------
    def dispense_fact(self):
        self.logger.log("Machine: preparing to dispense fact with printing set to: %s" % self.print_facts)
#         adventure = self.get_adventure()
        self.fact_count = self.fact_count + 1
        if self.print_facts == True:
            self.printer.printfact()

    def dispense_badge(self):
            self.logger.log("Machine: preparing to dispense fact with printing set to: %s" % self.print_facts)
    #         adventure = self.get_adventure()
            self.badge_count = self.badge_count + 1
            if self.print_facts == True:
                self.printer.printBadge()

    def start(self):
        self.logger.log("Machine: starting")
        self.__start_waiting_for_user()

    def stop(self):
        self.logger.log("Machine: stopping")
        self.waiting_to_print = False
