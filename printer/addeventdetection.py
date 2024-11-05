import RPi.GPIO as GPIO


def add_event_detection(pin, callback, bothdirections=False, pullup=False):
    try:
        pull_up_down = GPIO.PUD_UP if pullup else GPIO.PUD_DOWN
        if bothdirections:
            edge = GPIO.BOTH
        elif pullup:
            edge = GPIO.FALLING
        else:
            edge = GPIO.RISING
        edge = GPIO.BOTH if bothdirections else GPIO.RISING
        GPIO.setup(pin, GPIO.IN, pull_up_down=pull_up_down)
        GPIO.remove_event_detect(pin)
        GPIO.add_event_detect(pin, edge, callback=callback)
    except RuntimeError:
        # try:
        GPIO.remove_event_detect(pin)
        GPIO.add_event_detect(pin, edge, callback=callback)
        # except RuntimeError as e:
        #     pass
        #     print(f"Error during Event Detection: {e}")
