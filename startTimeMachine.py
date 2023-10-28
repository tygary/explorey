from timemachine.TimeMachineControls import *
import time

print("Machine started, enter 'machine.stop()' before exiting")

timemachine = TimeMachineControls()

while True:
    timemachine.update()
    time.sleep(0.05)
    continue
