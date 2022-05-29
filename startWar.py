from sound.MusicControlSystem import MusicControlSystem
from lighting.ExploreyLights import ExploreyLights
from lighting.WarGame import WarGame

# machine = Explorey()
# machine.start()
# machine.dispense_badge()

print("Machine started, enter 'machine.stop()' before exiting")

# music = MusicControlSystem()
# music.play_cave_ambient()
# print("Starting Music")

lighting = ExploreyLights(False)
lighting.start()

war = WarGame(lighting)

while True:
    continue
