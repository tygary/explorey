from printer.AdventureGenerator import AdventureGenerator
#from sound.MusicControlSystem import MusicControlSystem
#from lighting.ExploreyLights import *
import time

machine = AdventureGenerator()
machine.start()
# machine.dispense_badge()

print("Machine started, enter 'machine.stop()' before exiting")

#music = MusicControlSystem()
#music.play_bowling()
#print("Starting Music")

#lighting = ExploreyLights(MODE_PRINT)
#lighting.start()

while True:
    time.sleep(0.05)
    continue
