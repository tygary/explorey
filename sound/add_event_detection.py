import RPi.GPIO as GPIO
#from lib import fakeGPIO as GPIO


def add_event_detection(pin, callback, bothdirections=False, pullup=False):
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP if pullup else GPIO.PUD_DOWN)
        GPIO.remove_event_detect(pin)
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