from babel.BabelController import BabelController
import time

controller = BabelController(pigeon=False)
controller.start()

while True:
    time.sleep(0.05)
    continue
