import time
import serial


class DmxPyFt232:
    """Raw DMX512 driver for FT232RL RS485 adapters.

    Unlike the Enttec which has its own USB protocol, this adapter is a
    straight UART-to-RS485 converter. DMX512 requires 250kbaud 8N2 plus
    a hardware BREAK signal before each frame.
    """

    def __init__(self, port):
        self.serial = serial.Serial(
            port,
            baudrate=250000,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            rtscts=False,
            dsrdtr=False,
        )
        # Most FT232RL RS485 modules tie DE (Driver Enable) to RTS.
        # Assert it once so the chip stays in transmit mode.
        self.serial.rts = True
        # Index 0 = DMX start code (0x00), indices 1-512 = channels
        self._data = bytearray(513)

    def set_channel(self, chan, intensity):
        chan = max(0, min(512, chan))
        intensity = max(0, min(255, intensity))
        self._data[chan] = intensity

    def blackout(self):
        for i in range(1, 513):
            self._data[i] = 0

    def render(self):
        # BREAK: line held low for >=88µs (use 100µs for margin)
        self.serial.break_condition = True
        time.sleep(0.0001)
        # MAB (Mark After Break): line returns high for >=8µs
        self.serial.break_condition = False
        time.sleep(0.000012)
        # Start code (0x00) + 512 channel values
        self.serial.write(bytes(self._data))
