from lighting.ExploreyLights import *
import time

print("Machine started, enter 'machine.stop()' before exiting")

lighting = ExploreyLights(MODE_BEACON)
lighting.start()

while True:
    time.sleep(0.05)
    continue
