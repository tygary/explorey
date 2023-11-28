from timemachine.TimeMachineControls import *
import time

print("Machine started, enter 'machine.stop()' before exiting")

timemachine = TimeMachineControls()

while True:
    try:
        timemachine.update()
    except Exception as err:
        print(err)

    time.sleep(0.05)
    continue
