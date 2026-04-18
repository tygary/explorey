import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

SMALL = "small"
LARGE = "large"


class I2CDisplay:
    def __init__(self, multiplexor, port: int, size: str = SMALL, addr=0x3C, reset=None):
        self._size = size
        channel = multiplexor.channel(port)
        height = 64 if size == LARGE else 32
        # external_vcc=True changes the init sequence which resolves COM pin ghosting on SSD1309
        self._oled = adafruit_ssd1306.SSD1306_I2C(128, height, channel, addr=addr, reset=reset, external_vcc=size == LARGE)

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

        self._oled.fill(0)
        self._oled.show()
        self._oled.image(image)
        self._oled.show()
