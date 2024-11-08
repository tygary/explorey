from ghost.ScaleMachine import GhostScaleMachine
import time

print("Ghost scale started, enter 'machine.stop()' before exiting")

machine = GhostScaleMachine()

while True:
    #try:
    machine.update()
    #except Exception as err:
    #    print(err)

    time.sleep(0.01)
    continue
