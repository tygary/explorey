import RPi.GPIO as GPIO
import threading


class LeverInputController(object):
    pins = [31, 33, 35, 37]
    currentValues = [1, 1, 1, 1]
    callback = None
    thread = None
    logger = None

    def __init__(self, callback, logger):
        self.logger = logger
        for pin in self.pins:
            self.setup_pin(pin)
        self.callback = callback
        # self.thread = threading.Thread(target=self.thread_fn, args=(1,))
        self.add_event_detection(self.pins[0], self.callback, bothdirections=True)
        self.add_event_detection(self.pins[1], self.callback, bothdirections=True)
        self.add_event_detection(self.pins[2], self.callback, bothdirections=True)
        self.add_event_detection(self.pins[3], self.callback, bothdirections=True)

    def setup_pin(self, pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(pin)

    def add_event_detection(self, pin, callback, bothdirections=False):
        try:
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=callback)
            if bothdirections:
                GPIO.add_event_detect(pin, GPIO.RISING, callback=callback)
        except RuntimeError:
            try:
                GPIO.remove_event_detect(pin)
                GPIO.add_event_detect(pin, GPIO.FALLING, callback=callback)
                if bothdirections:
                    GPIO.add_event_detect(pin, GPIO.RISING, callback=callback)
            except RuntimeError:
                pass

    def check_for_new_switch_values(self):
        changed = False
        newValues = [1, 1, 1, 1]
        for i in range(4):
            newValues[i] = GPIO.input(self.pins[i])
            if newValues[i] != self.currentValues[i]:
                changed = True
                self.logger.log("Lever %d changed to %d" % (i, newValues[i]))
                self.currentValues[i] = newValues[i]

        if changed:
            self.callback(self.currentValues)

    def thread_fn(self):
        while True:
            self.check_for_new_switch_values()
