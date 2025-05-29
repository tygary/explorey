from bank.FoundersBox import FoundersBox
import time

print("Bank Founders Box started, enter 'machine.stop()' before exiting")

machine = FoundersBox()

while True:
    try:
        machine.update()
    except Exception as err:
        print(err)

    time.sleep(0.05)
    continue
