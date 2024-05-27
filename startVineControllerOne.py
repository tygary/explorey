from ratlantis.RatVineController import RatVineController
import time

print("Rat Controller one started, enter 'machine.stop()' before exiting")

vine_controller_one = RatVineController(controller_num=1)

while True:
    try:
        vine_controller_one.update()
    except Exception as err:
        print(err)
    time.sleep(0.05)
    continue
