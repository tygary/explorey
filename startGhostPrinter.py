from ghost.PrinterMachine import PrinterMachine
import time

print("Ghost Printer started, enter 'machine.stop()' before exiting")

machine = PrinterMachine()

while True:
    #try:
    machine.update()
    #except Exception as err:
    #    print(err)

    time.sleep(0.05)
    continue
