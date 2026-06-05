import logging
import time

from babel.BabelController import BabelController

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-5s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)

controller = BabelController(pigeon=True)
controller.start()

while True:
    time.sleep(0.05)
    continue
