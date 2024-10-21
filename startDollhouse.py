from ghost.Dollhouse import Dollhouse
import time

print("Dollhouse started, enter 'machine.stop()' before exiting")

dollhouse = Dollhouse()

while True:
    #try:
    dollhouse.update()
    #except Exception as err:
    #    print(err)

    time.sleep(0.05)
    continue
