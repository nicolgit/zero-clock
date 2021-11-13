import digitalio
import busio
import board

from PIL import Image, ImageDraw, ImageFont

from adafruit_epd.il0373 import Adafruit_IL0373
from adafruit_epd.il91874 import Adafruit_IL91874  # pylint: disable=unused-import
from adafruit_epd.il0398 import Adafruit_IL0398    # pylint: disable=unused-import
from adafruit_epd.ssd1608 import Adafruit_SSD1608  # pylint: disable=unused-import
from adafruit_epd.ssd1675 import Adafruit_SSD1675  # pylint: disable=unused-import
from adafruit_epd.ssd1680 import Adafruit_SSD1680  # pylint: disable=unused-import
from adafruit_epd.ssd1681 import Adafruit_SSD1681  # pylint: disable=unused-import

from adafruit_epd.epd import Adafruit_EPD


class ClockView(object):
    def __init__(self):
        # UI Constants
        WHITE = (0xFF, 0xFF, 0xFF)
        BLACK = (0x00, 0x00, 0x00)
        
        self.BORDER = 10
        self.FONTSIZE_BIG = 32
        self.FONTSIZE_HUGE = 64
        self.BACKGROUND_COLOR = WHITE
        self.FOREGROUND_COLOR = BLACK
        self.TEXT_COLOR = BLACK


        # create the spi device and pins we will need
        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self.ecs = digitalio.DigitalInOut(board.CE0)
        self.dc = digitalio.DigitalInOut(board.D22)
        self.srcs = None
        self.rst = digitalio.DigitalInOut(board.D27)
        self.busy = digitalio.DigitalInOut(board.D17)

        self.font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", self.FONTSIZE_BIG)
        self.font_huge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", self.FONTSIZE_HUGE)

        self.display = Adafruit_SSD1675(122, 250, 
            self.spi,
            cs_pin=self.ecs,
            dc_pin=self.dc,
            sramcs_pin=self.srcs,
            rst_pin=self.rst,
            busy_pin=self.busy,
        )

        self.display.rotation = 1
        self.display.fill(Adafruit_EPD.WHITE)
        self.display.display()


    def show_time(self, time):        
        print("its " + time + "!")
        text = time

        (font_width, font_height) = self.font_big.getsize(text)

        img_width = font_width
        img_height = font_height
        img_x = (self.display.width-img_width)/2
        img_y = (self.display.height-img_height)/2

        image = Image.new("RGB", (self.display.width, self.display.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.display.width - 1, self.display.height - 1), fill=self.BACKGROUND_COLOR)

        
        draw.text(
            (img_x, img_y),
            text,
            font=self.font_big,
            fill=self.FOREGROUND_COLOR,
        )

        self.display.image(image)
        self.display.display()
        

    def show_welcome(self):
        text = "Hello!"

        image = Image.new("RGB", (self.display.width, self.display.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.display.width - 1, self.display.height - 1), fill=self.BACKGROUND_COLOR)

        (font_width, font_height) = self.font_huge.getsize(text)
        draw.text(
            (self.display.width // 2 - font_width // 2, self.display.height // 2 - font_height // 2),
            text,
            font=self.font_huge,
            fill=self.FOREGROUND_COLOR,
        )

        self.display.image(image)
        self.display.display()


