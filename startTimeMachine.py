from timemachine.TimeMachine import *
import time

print("Machine started, enter 'machine.stop()' before exiting")

timemachine = TimeMachine()

while True:
    timemachine.update()
    time.sleep(0.05)
    continue
