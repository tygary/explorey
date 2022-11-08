from printer.Bats import Bats
from sound.MusicControlSystem import MusicControlSystem
#from lighting.ExploreyLights import *
import time

#machine = Bats()
#machine.start()
# machine.dispense_badge()

print("Machine started, enter 'machine.stop()' before exiting")

music = MusicControlSystem()
music.play_bats_ambient()
print("Starting Music")

#lighting = ExploreyLights(MODE_PRINT)
#lighting.start()

while True:
    time.sleep(0.05)
    continue
