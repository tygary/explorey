from printer.Explorey import Explorey
from sound.MusicControlSystem import MusicControlSystem
from lighting.ExploreyLights import *

machine = Explorey()
machine.start()
# machine.dispense_badge()

print("Machine started, enter 'machine.stop()' before exiting")

music = MusicControlSystem()
music.play_cave_ambient()
print("Starting Music")

lighting = ExploreyLights(MODE_PRINT)
lighting.start()

while True:
    continue
