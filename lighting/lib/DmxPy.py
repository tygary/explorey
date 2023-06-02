import serial, sys, time


DMXOPEN = chr(126)
DMXCLOSE = chr(231)
DMXINTENSITY = chr(6) + chr(1) + chr(2)
DMXINIT1 = chr(3) + chr(2) + chr(0) + chr(0) + chr(0)
DMXINIT2 = chr(10) + chr(2) + chr(0) + chr(0) + chr(0)


class DmxPy:
    def __init__(self, serialPort):
        try:
            self.serial = serial.Serial(serialPort, baudrate=57600)
        except:
            print("Error: could not open Serial Port")
            sys.exit(0)
        b = bytearray()
        b.extend((DMXOPEN + DMXINIT1 + DMXCLOSE).encode())
        b.extend(serial.encode())
        b.extend(data)
        b.extend()
        self.serial.write(b)
        b = bytearray()
        b.extend((DMXOPEN + DMXINIT2 + DMXCLOSE).encode())
        self.serial.write(b)

        self.dmxData = [chr(0).encode()] * 513  # 128 plus "spacer".

    def setChannel(self, chan, intensity):
        if chan > 512:
            chan = 512
        if chan < 0:
            chan = 0
        if intensity > 255:
            intensity = 255
        if intensity < 0:
            intensity = 0
        self.dmxData[chan] = intensity.to_bytes(1, byteorder="big")

    def blackout(self):
        for i in range(1, 512, 1):
            self.dmxData[i] = chr(0)

    def render(self):
        data = bytearray()
        for value in self.dmxData:
            data.extend(value)
        b = bytearray()
        b.extend(DMXOPEN.encode())
        b.extend(DMXINTENSITY.encode())
        b.extend(data)
        b.extend(DMXCLOSE.encode())
        print(b)
        self.serial.write(b)
