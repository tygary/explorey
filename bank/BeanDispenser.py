import time
import RPi.GPIO as GPIO


TIME_ON_S = 0.1
TIME_BETWEEN_ON_S = 0.1

class BeanDispenser(object):
    def __init__(self, pin):
        self.amount_left = 0
        self.pin = pin

        self.on_time = 0
        self.off_time = 0
        self.state = 0

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        print(f"Dispensing beans...")
        self.on_time = time.time()
        self.state = 1
        
    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.off_time = time.time()
        self.state = 0


    def dispense(self, amount):
        """
        Dispenses the specified amount of beans.
        :param amount: The number of beans to dispense.
        """
        if amount <= 0:
            print("Invalid amount to dispense:", amount)
            return
        self.amount_left = amount + 1  
        print(f"Dispensing {amount} beans...")

    def update(self):
        now = time.time()
        if self.state == 0 and self.amount_left > 0 and now > self.off_time + TIME_BETWEEN_ON_S:
            self.on()
            self.amount_left -= 1
        elif self.state == 1 and now > self.on_time + TIME_ON_S:
            self.off()
            if self.amount_left <= 0:
                print("Dispensing complete.")
