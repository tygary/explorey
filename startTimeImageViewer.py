from timemachine.TimeImageViewer import TimeImageViewer
import time

print("Machine started, enter 'machine.stop()' before exiting")


viewer = TimeImageViewer()

while True:
    try:
        viewer.tick()
    except Exception as err:
        print(err)
    time.sleep(0.05)
    continue
