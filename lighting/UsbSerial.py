import serial


class UsbSerial(object):
    serial = None

    def __init__(self, port="/dev/ttyACM0"):
        self.serial = serial.Serial(port, 9600, timeout=5)
        # self.serial.open()

    def read(self):
        return self.serial.readLine()

    def write(self, message):
        self.serial.flushOutput()
        return self.serial.write(message)

    def close(self):
        self.serial.close()