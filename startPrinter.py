from printer.Explorey import Explorey
from sound.MusicControlSystem import MusicControlSystem

machine = Explorey()
machine.start()
# machine.dispense_badge()

print("Machine started, enter 'machine.stop()' before exiting")

music = MusicControlSystem()
print("Starting Music")
