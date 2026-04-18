import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

SMALL = "small"
LARGE = "large"


_SSD1309_INIT = (
    0xAE,        # display off
    0xD5, 0x80,  # clock divide ratio
    0xA8, 63,    # multiplex ratio (64 rows)
    0xD3, 0x90,  # display offset
    0x40,        # start line
    0x20, 0x00,  # memory addressing mode: horizontal
    0xA1,        # segment remap
    0xC8,        # COM scan direction: normal top-to-bottom (0xC8 remapped + sequential causes half-swap)
    0xDA, 0x12,  # COM pins: alternative
    0x81, 0x8F,  # contrast (reduced from 0xFF to limit bleed)
    0xD9, 0x22,  # pre-charge period
    0xDB, 0x20,  # VCOMH deselect level (lowered from 0x34 to reduce ghost voltage)
    0xA4,        # output follows RAM
    0xA6,        # normal display
    0xAF,        # display on
)


class _SSD1309_I2C(adafruit_ssd1306.SSD1306_I2C):
    """SSD1306 subclass with correct SSD1309 init (no charge pump, sequential COM pins)."""

    def init_display(self):
        for cmd in _SSD1309_INIT:
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def __init__(self, width, height, i2c, **kwargs):
        super().__init__(width, height, i2c, **kwargs)
        # Belt-and-suspenders: re-send in case init_display isn't called by this library version
        for cmd in _SSD1309_INIT:
            self.write_cmd(cmd)


class I2CDisplay:
    def __init__(self, multiplexor, port: int, size: str = SMALL, addr=0x3C, reset=None):
        self._size = size
        channel = multiplexor.channel(port)
        height = 64 if size == LARGE else 32
        cls = _SSD1309_I2C if size == LARGE else adafruit_ssd1306.SSD1306_I2C
        self._oled = cls(128, height, channel, addr=addr, reset=reset)

        self._oled.fill(0)
        self._oled.show()

    def displayText(self, text: str):
        image = Image.new("1", (self._oled.width, self._oled.height))
        draw = ImageDraw.Draw(image)

        draw.rectangle((0, 0, self._oled.width, self._oled.height), fill=0)

        font = ImageFont.load_default()
        bbox = font.getbbox(text)
        font_width = bbox[2] - bbox[0]
        font_height = bbox[3] - bbox[1]
        draw.text(
            (self._oled.width // 2 - font_width // 2, self._oled.height // 2 - font_height // 2),
            text,
            font=font,
            fill=255,
        )

        self._oled.image(image)
        self._oled.show()
