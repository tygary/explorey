import RPi.GPIO as GPIO

class GenericButtonController(object):

    assignments = None

    def __init__(self):
        assignments = []

    def setup_pin(self, pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(pin)

    def add_event_detection(self, pin, callback, bothdirections=False):
        self.setup_pin(pin)
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
