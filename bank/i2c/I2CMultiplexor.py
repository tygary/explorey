import board
import adafruit_tca9548a


class I2CMultiplexor:
    def __init__(self, address=0x70):
        self._i2c = board.I2C()
        self._tca = adafruit_tca9548a.TCA9548A(self._i2c, address=address)

    def channel(self, port: int):
        return self._tca[port]
