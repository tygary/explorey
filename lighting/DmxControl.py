from dmxpy import DmxPy
import time


class DmxControl(object):
    dmx = None

    def __init__(self):
        self.dmx = DmxPy.DmxPy("/dev/ttyUSB0")

    def setLight(self, channelStart, color):
        self.dmx.set_channel(channelStart, color[0])
        self.dmx.set_channel(channelStart + 1, color[1])
        self.dmx.set_channel(channelStart + 2, color[2])
        # print("set light {} to color {}".format(channelStart, color))

    def setParCan(self, channelStart, color):
        self.dmx.set_channel(channelStart, color[0])
        self.dmx.set_channel(channelStart + 1, color[1])
        self.dmx.set_channel(channelStart + 2, color[2])
        self.dmx.set_channel(channelStart + 3, 255)
        self.dmx.set_channel(channelStart + 4, 255)

    def set4barFlex(self, channelStart, colors=[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]):
        self.dmx.set_channel(channelStart, 0)  # Color Mode RGB
        self.dmx.set_channel(channelStart + 1, 255)  # Brightness max
        self.dmx.set_channel(channelStart + 2, 0)  # strobe 0

        self.dmx.set_channel(channelStart + 3, colors[0][0])
        self.dmx.set_channel(channelStart + 4, colors[0][1])
        self.dmx.set_channel(channelStart + 5, colors[0][2])
        self.dmx.set_channel(channelStart + 6, colors[1][0])
        self.dmx.set_channel(channelStart + 7, colors[1][1])
        self.dmx.set_channel(channelStart + 8, colors[1][2])
        self.dmx.set_channel(channelStart + 9, colors[2][0])
        self.dmx.set_channel(channelStart + 10, colors[2][1])
        self.dmx.set_channel(channelStart + 11, colors[2][2])
        self.dmx.set_channel(channelStart + 12, colors[3][0])
        self.dmx.set_channel(channelStart + 13, colors[3][1])
        self.dmx.set_channel(channelStart + 14, colors[3][2])

    def setDimmer(self, channel, brightness):
        self.dmx.set_channel(channel, brightness)

    def render(self):
        self.dmx.render()

    def blackout(self):
        self.dmx.blackout()
        self.dmx.render()

    def setBlackLight(self, channelStart, brightness):
        # Blacklight channels
        # 1  -  0 for dmx control
        # 2  -  0 for full color?
        # 3  -  Speed.  Set to 0?
        # 4  -  Total Brightness 0-255
        # 5  -  Red
        # 6  -  Green
        # 7  -  Blue
        self.dmx.set_channel(channelStart, 0)
        self.dmx.set_channel(channelStart + 1, 0)
        self.dmx.set_channel(channelStart + 2, 0)
        self.dmx.set_channel(channelStart + 3, brightness)
        self.dmx.set_channel(channelStart + 4, 255)
        self.dmx.set_channel(channelStart + 5, 255)
        self.dmx.set_channel(channelStart + 6, 255)
        # print("set blacklight {} to brightness {}".format(channelStart, brightness))
