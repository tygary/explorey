from sound.MusicControlSystem import MusicControlSystem
from lighting.ExploreyLights import *
from lighting.WarGame import WarGame
import time

# machine = Explorey()
# machine.start()
# machine.dispense_badge()

print("Machine started, enter 'machine.stop()' before exiting")

music = MusicControlSystem()
music.play_space()
print("Starting Music")

lighting = ExploreyLights(MODE_WAR)
lighting.start()

war = WarGame(lighting)
war.start()

while True:
    time.sleep(0.05)
    continue
