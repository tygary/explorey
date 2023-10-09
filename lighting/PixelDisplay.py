from lighting.lib.led_matrix import Matrix
import board
import neopixel
from adafruit_pixel_framebuf import PixelFramebuffer, VERTICAL

class PixelDisplay(object):
    matrix = Matrix()
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
        #self.matrix.reset()
        #self.matrix.text(text, (0, 0), 8, (255, 0, 0))
        #self.matrix.show()

