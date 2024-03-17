from ratlantis.RatGame import RatGame
import time

print("Rat Game started, enter 'machine.stop()' before exiting")

rat_game = RatGame()

while True:
    try:
        rat_game.update()
    except Exception as err:
        print(err)

    time.sleep(0.05)
    continue
