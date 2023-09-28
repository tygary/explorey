from printer.AdventureGenerator import AdventureGenerator
#from sound.MusicControlSystem import MusicControlSystem
#from lighting.ExploreyLights import *
from timemachine.Levers import Levers
import time

# machine = AdventureGenerator()
# machine.start()
# machine.dispense_badge()

print("Machine started, enter 'machine.stop()' before exiting")

#music = MusicControlSystem()
#music.play_bowling()
#print("Starting Music")

#lighting = ExploreyLights(MODE_PRINT)
#lighting.start()

def on_lever_change(id, value):
    print(f"Got lever {id} change to {value}")

def on_button_change(id, value):
    print(f"Got button {id} change to {value}")


levers = Levers(on_lever_change, on_button_change)


while True:
    levers.update()
    time.sleep(0.05)
    continue
