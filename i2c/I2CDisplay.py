import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

SMALL = "small"
LARGE = "large"


class _SSD1309_I2C(adafruit_ssd1306.SSD1306_I2C):
    """SSD1306 subclass that re-runs correct SSD1309 init (no charge pump)."""

    def __init__(self, width, height, i2c, **kwargs):
        super().__init__(width, height, i2c, **kwargs)
        for cmd in (
            0xAE,              # display off
            0xD5, 0x80,        # clock divide ratio
            0xA8, height - 1,  # multiplex ratio
            0xD3, 0x00,        # display offset
            0x40,              # start line
            0xA1,              # segment remap
            0xC8,              # COM scan direction
            0xDA, 0x12,        # COM pins config (no charge pump unlike SSD1306)
            0x81, 0xFF,        # contrast
            0xD9, 0x22,        # pre-charge period
            0xDB, 0x34,        # VCOMH deselect level
            0xA4,              # output follows RAM
            0xA6,              # normal display
            0xAF,              # display on
        ):
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
