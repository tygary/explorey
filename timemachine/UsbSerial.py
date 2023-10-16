import serial
import glob


class UsbSerial(object):
    serial = None
    is_connected = False
    enabled = True

    def __init__(self, port="/dev/ttyACM0"):
        self.port = port
        self.__check_connection()
        # self.serial.open()

    def disable(self):
        self.enabled = False

    def read(self):
        if not self.enabled:
            return
        self.__check_connection()
        if self.is_connected and self.serial.in_waiting > 0:
            return self.serial.read_until()

    def __check_connection(self):
        if not self.enabled:
            return
        if self.is_connected:
            try:
                self.serial.inWaiting()
            except:
                print("Lost connection!")
                self.is_connected = False
        else:
            try:
                ports = glob.glob('/dev/ttyACM*')
                if len(ports) > 0:
                    print(ports)
                    self.port = ports[0]
                self.serial = serial.Serial(self.port, 9600, timeout=5)
                print("Connected!")
                self.is_connected = True
            except Exception as err:
                print(f"Failed to Connect - {err}")
                self.is_connected = False

    def write(self, message):
        if not self.enabled:
            return
        self.__check_connection()
        if self.is_connected:
            if self.serial.out_waiting > 100:
                self.serial.reset_output_buffer()
            return self.serial.write(message)

    def close(self):
        if not self.enabled:
            return
        if self.is_connected:
            self.serial.close()