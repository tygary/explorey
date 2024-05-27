import RPi.GPIO as GPIO
import random

from lighting.routines import Routines
from ratlantis.Artifact import Artifact
from ratlantis.EnergyVine import *
from ratlantis.EnergyTank import EnergyTank
from ratlantis.GameLogic import GameLogic
from lighting.PixelControl import PixelControl
from mqtt.MqttClient import MqttClient

TEST_RFID = "2dcc1366080104e0"


class RatVineController(object):
    pixels = None
    mqtt = None

    vines = []

    def __init__(self, controller_num=1):
        GPIO.setmode(GPIO.BCM)
        self.pixels = PixelControl(700, led_brightness=180, led_pin=21)
        self.mqtt = MqttClient()

        if controller_num == 1:
            vine1 = EnergyVine(VINE_ONE_RFID, range(0, 174), self.pixels, self.mqtt)
            vine1.pending_connection(COLOR_BLUE)
            self.vines.append(vine1)
            vine2 = EnergyVine(VINE_TWO_RFID, range(174, 349), self.pixels, self.mqtt)
            vine2.pending_connection(COLOR_ORANGE)
            self.vines.append(vine2)
            vine3 = EnergyVine(VINE_THREE_RFID, range(349, 523), self.pixels, self.mqtt)
            vine3.pending_connection(COLOR_PINK)
            self.vines.append(vine3)
            vine4 = EnergyVine(VINE_FOUR_RFID, range(523, 697), self.pixels, self.mqtt)
            vine4.pending_connection(COLOR_GREEN)
            self.vines.append(vine4)
        elif controller_num == 2:
            vine1 = EnergyVine(VINE_FIVE_RFID, range(0, 174), self.pixels, self.mqtt)
            vine1.pending_connection(COLOR_YELLOW)
            self.vines.append(vine1)
            vine2 = EnergyVine(VINE_SIX_RFID, range(174, 349), self.pixels, self.mqtt)
            vine2.pending_connection(COLOR_PURPLE)
            self.vines.append(vine2)
            vine3 = EnergyVine(VINE_SEVEN_RFID, range(349, 523), self.pixels, self.mqtt)
            vine3.pending_connection(COLOR_LIGHT_BLUE)
            self.vines.append(vine3)
            vine4 = EnergyVine(VINE_EIGHT_RFID, range(523, 697), self.pixels, self.mqtt)
            vine4.pending_connection(COLOR_RED)
            self.vines.append(vine4)

    def update(self):
        for vine in self.vines:
            vine.update()
        self.pixels.render()





