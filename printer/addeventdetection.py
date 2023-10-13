import RPi.GPIO as GPIO


def add_event_detection(pin, callback, bothdirections=False, pullup=False):
    try:
        pull_up_down = GPIO.PUD_UP if pullup else GPIO.PUD_DOWN
        GPIO.setup(pin, GPIO.IN, pull_up_down=pull_up_down)
        GPIO.remove_event_detect(pin)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=callback)
        if bothdirections:
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=callback)
    except RuntimeError:
        try:
            GPIO.remove_event_detect(pin)
            GPIO.add_event_detect(pin, GPIO.RISING, callback=callback)
            if bothdirections:
                GPIO.add_event_detect(pin, GPIO.FALLING, callback=callback)
        except RuntimeError:
            pass
            print("Error during Event Detection")
