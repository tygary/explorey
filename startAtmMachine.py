import time
from bank.ATMMachine import ATMMachine
import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'

machine = ATMMachine()
machine.start()

print("Machine started, enter 'machine.stop()' before exiting")

# while True:
#     time.sleep(0.05)
#     machine.update()
#     continue
