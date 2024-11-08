import time
from rpi_ws281x import *
import uuid


class PixelControl(object):
    # LED strip configuration:
    LED_COUNT = 300  # Number of LED pixels.
    # LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_PIN = 10  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 200  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = (
        False  # True to invert the signal (when using NPN transistor level shift)
    )
    LED_CHANNEL = 0
    #     LED_STRIP = ws.SK6812_STRIP_RGBW

    def __init__(self, led_count=300, led_brightness=200, led_pin=21, led_dma=10):
        self.LED_COUNT = led_count
        self.LED_PIN = led_pin
        self.LED_DMA = led_dma
        self.LED_BRIGHTNESS = led_brightness
        self.strip = Adafruit_NeoPixel(
            self.LED_COUNT,
            self.LED_PIN,
            self.LED_FREQ_HZ,
            self.LED_DMA,
            self.LED_INVERT,
            self.LED_BRIGHTNESS,
            self.LED_CHANNEL,
        )
        self.strip.begin()

    def setColor(self, channel, color):
        self.strip.setPixelColor(channel, Color(color[1], color[0], color[2]))

    def setRGBW(self, channel, values):
        self.strip.setPixelColor(
            channel, Color(values[1], values[0], values[2], values[3])
        )

    def blackout(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0, 0))
        self.strip.show()

    def render(self):
        self.strip.show()


# try:
#     num = 1
#     #while True:
#     colorWipe(strip, Color(0,0,0))
#     rainbowCycle(strip)
#     #strip.setPixelColor(0, Color(255,50,50))
#     #strip.show()
#     #num += 1
# except KeyboardInterrupt:
#     colorWipe(strip, Color(0,0,0), 10)


class SubPixelControl(object):

    def __init__(self, num_pixels, add_pending_change, on_render, routine, should_override=False):
        self.num_pixels = num_pixels
        self.add_pending_change = add_pending_change
        self.on_render = on_render
        self.routine = routine
        self.should_override = should_override
        self.uuid = str(uuid.uuid4())
        self.pixels = [(0, 0, 0, 0) for i in range(num_pixels)]

    def setColor(self, channel, color):
        self.pixels[channel] = (color[0], color[1], color[2], 0)
        self.add_pending_change(self)

    def setRGBW(self, channel, values):
        self.pixels[channel] = (values[0], values[1], values[2], values[3])
        self.add_pending_change(self)

    def blackout(self):
        for i in range(self.num_pixels):
            self.pixels[i] = (0, 0, 0, 0)
        self.add_pending_change(self)
        self.on_render()

    def render(self):
        self.on_render()


class OverlayedPixelControl(object):

    pending_routines = []

    def __init__(self, led_count=300, led_brightness=200, led_pin=21, led_dma=10):
        self.pixels = PixelControl(led_count, led_brightness, led_pin, led_dma)

    def get_sub_pixels_for_routine(self, routine, should_override=False):
        return SubPixelControl(self.pixels.strip.numPixels(), self.add_pending_change, self.pixels.render, routine, should_override)

    def add_pending_change(self, sub_pixel_routine):
        if sub_pixel_routine not in self.pending_routines:
            self.pending_routines.append(sub_pixel_routine)

    def _add_color(self, prev_value, new_value):
        return min(prev_value + new_value, 255)

    def render(self):
        for i in range(self.pixels.strip.numPixels()):
            value = [0, 0, 0, 0]
            for routine in self.pending_routines:
                if routine.should_override:
                    value = routine.pixels[i]
                else:
                    routine_value = routine.pixels[i]
                    value = [
                        self._add_color(value[0], routine_value[0]),
                        self._add_color(value[1], routine_value[1]),
                        self._add_color(value[2], routine_value[2]),
                        self._add_color(value[3], routine_value[3]),
                    ]
            self.pixels.setRGBW(i, value)
        self.pending_routines = []
        self.pixels.strip.show()

