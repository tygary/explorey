import threading
from printer.addeventdetection import *
from logger.logger import Logger


# -----------------------------------------------------------------------
# Coin Machine
# -----------------------------------------------------------------------
class CoinMachine(object):
    coin_input_pin = 27
    coin_counter_input_pin = 18
    # coin_counter_pins = [29, 31]

    waiting_for_coin = False
    accepted_a_coin = False

    coin_detected = False
    coin_counted = False
    coin_pending = False
    demo_mode = False

    current_value = 0

    callback = None

    logger = None

    def __init__(self, demo_mode=False):
        self.logger = Logger()
        self.demo_mode = demo_mode
        #GPIO.setup(self.coin_counter_pins, GPIO.OUT)
        self.__set_coin_count(0)

    # Public --------------------------------------------

    def start_waiting_for_coin(self, callback):
        if callback:
            self.callback = callback
        self.logger.log("Coin: waiting for coin at pin %s" % self.coin_input_pin)
        add_event_detection(self.coin_input_pin, callback=self.__coin_cb, pullup=False, bothdirections=True)
        add_event_detection(self.coin_counter_input_pin, callback=self.__coin_counter_cb, pullup=False, bothdirections=True)
        self.waiting_for_coin = True

    def clear_coins(self):
        self.logger.log("Coin: clearing count")
        self.__set_coin_count(0)

    def subtract_coins(self, num):
        self.logger.log("Coin: new coin count = %s - %s" % (self.current_value, num))
        self.__set_coin_count(self.current_value - num)

    # Private -------------------------------------------

    def __coin_cb(self, channel):
        self.logger.log("Coin: coin cb with waiting status: %s" % self.waiting_for_coin)
        if self.waiting_for_coin is True:
            self.__coin_detected()
            self.coin_detected = True

    def __coin_counter_cb(self, channel):
        self.logger.log("Coin: coin counter cb with waiting status: %s" % self.waiting_for_coin)
        if self.waiting_for_coin is True:
            self.__coin_detected()
            self.coin_counted = True

    def __coin_detected(self):
        self.logger.log("Coin: coin detected with pending status: %s" % self.coin_pending)
        if self.coin_pending is False:
            self.coin_pending = True
            self.coin_detected = False
            self.coin_counted = False
            t = threading.Timer(1.0, self.__done_waiting_for_coin)
            t.start()

    def __done_waiting_for_coin(self):
        self.logger.log("Coin: done waiting with pending status")
        self.coin_detected = True
        #Fake the coin detection for now, it's broken
        if self.coin_detected is True: # and self.coin_counted is True:
            # self.logger.log("  Got a coin, pick a box")
            self.__set_accepted_coin(True)
        else:
            self.logger.log("  Not accepted")
        self.coin_detected = False
        self.coin_counted = False
        self.coin_pending = False

    def __wait_for_coin(self):
        self.logger.log("Coin: waiting_for_coin set to true, was: %s" % self.waiting_for_coin)
        self.waiting_for_coin = True


    def __set_accepted_coin(self, value):
        self.logger.log("Coin: accepting coin with value %s" % value)
        self.accepted_a_coin = value
        if value is True:
            try:
                if self.demo_mode is True:
                    #If it's demo mode, then we should only allow 1 credit
                    self.__set_coin_count(1)
                else:
                    self.__set_coin_count(self.current_value + 1)
            except RuntimeError:
                self.logger.log("  error set_accepted_coin")
            if self.callback:
                self.callback()

    def __set_coin_count(self, count):
        self.logger.log("Coin: attempting to set count to %s from %s" % (count, self.current_value))
        #Don't allow more than three credits
        if count < 0:
            self.logger.log("  count below min, setting to min")
            count = 0
        if count > 3:
            self.logger.log("  count exceeds max, setting to max")
            count = 3
        self.logger.log("  setting count to %s" % count)
        self.current_value = count
        # if count == 3:
        #     GPIO.output(self.coin_counter_pins[0], True)
        #     GPIO.output(self.coin_counter_pins[1], True)
        # elif count == 2:
        #     GPIO.output(self.coin_counter_pins[0], False)
        #     GPIO.output(self.coin_counter_pins[1], True)
        # elif count == 1:
        #     GPIO.output(self.coin_counter_pins[0], True)
        #     GPIO.output(self.coin_counter_pins[1], False)
        # else:
        #     GPIO.output(self.coin_counter_pins[0], False)
        #     GPIO.output(self.coin_counter_pins[1], False)
