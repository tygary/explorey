import serial


class UsbSerial(object):
    serial = None
    is_connected = False

    def __init__(self, port="/dev/ttyACM0"):
        try:
            self.serial = serial.Serial(port, 9600, timeout=5)
            self.is_connected = True
        except:
            self.serial = None
            self.is_connected = False

        # self.serial.open()

    def read(self):
        if self.is_connected:
            return self.serial.readLine()

    def write(self, message):
        if self.is_connected:
            if self.serial.out_waiting > 100:
                self.serial.reset_output_buffer()
            return self.serial.write(message)

    def close(self):
        if self.is_connected:
            self.serial.close()