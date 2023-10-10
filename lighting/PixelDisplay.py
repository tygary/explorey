import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

class PixelDisplay(object):
    pixels = neopixel.NeoPixel(
        board.D21,
        8 * 128,
        brightness=0.2,
        auto_write=False,
    )
    buffer = PixelFramebuffer(
        pixels,
        128,
        8,
        orientation=VERTICAL,
    )
    def draw_text(self, text):
        self.buffer.fill(0x000000)
        self.buffer.text(text, 2, 0, 0xFF0000)
        self.buffer.display()

