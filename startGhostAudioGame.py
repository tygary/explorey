from ghost.AudioMachine import AudioMachine
import time

print("Dollhouse started, enter 'machine.stop()' before exiting")

machine = AudioMachine()

while True:
    #try:
    machine.update()
    #except Exception as err:
    #    print(err)

    time.sleep(0.05)
    continue