from ratlantis.RatVineController import RatVineController
import time

print("Rat Controller two started, enter 'machine.stop()' before exiting")

vine_controller_two = RatVineController(controller_num=2)

while True:
    try:
        vine_controller_two.update()
    except Exception as err:
        print(err)
    time.sleep(0.05)
    continue
