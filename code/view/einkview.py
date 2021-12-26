from view.baseview import BaseView

import busio
import board
import digitalio
import pyqrcode
import png

from pyqrcode import QRCode
from PIL import Image, ImageDraw, ImageFont

from adafruit_epd.il0373 import Adafruit_IL0373
from adafruit_epd.il91874 import Adafruit_IL91874  # pylint: disable=unused-import
from adafruit_epd.il0398 import Adafruit_IL0398    # pylint: disable=unused-import
from adafruit_epd.ssd1608 import Adafruit_SSD1608  # pylint: disable=unused-import
from adafruit_epd.ssd1675 import Adafruit_SSD1675  # pylint: disable=unused-import
from adafruit_epd.ssd1680 import Adafruit_SSD1680  # pylint: disable=unused-import
from adafruit_epd.ssd1681 import Adafruit_SSD1681  # pylint: disable=unused-import

from adafruit_epd.epd import Adafruit_EPD


class EinkView(BaseView):
    def __init__(self):
        # UI Constants
        WHITE = (0xFF, 0xFF, 0xFF)
        BLACK = (0x00, 0x00, 0x00)
        
        self.QRCODE_FILENAME = "/run/shm/qr.png"
        self.BORDER = 10
        self.FONTSIZE_MEDIUM = 18
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

        self.font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", self.FONTSIZE_MEDIUM)
        self.font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", self.FONTSIZE_BIG)
        self.font_huge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", self.FONTSIZE_HUGE)

        self.display = Adafruit_SSD1675(122, 250, 
            self.spi,
            cs_pin=self.ecs,
            dc_pin=self.dc,
            sramcs_pin=self.srcs,
            rst_pin=self.rst,
            busy_pin=self.busy,
        )

        self.display.rotation = 1
        self.image = None

        
        self.image = Image.new("RGB", (self.display.width, self.display.height))

        draw = ImageDraw.Draw(self.image)
        draw.rectangle((0, 0, self.display.width - 1, self.display.height - 1), fill=self.BACKGROUND_COLOR)
    
    def prepare_image(self):
        self.image = Image.new("RGB", (self.display.width, self.display.height))

        draw = ImageDraw.Draw(self.image)
        draw.rectangle((0, 0, self.display.width - 1, self.display.height - 1), fill=self.BACKGROUND_COLOR)
    
    def show_qrcode(self, urlstring, x, y):
        url = pyqrcode.create(urlstring)
        print(url.get_png_size(1))

        url.png(self.QRCODE_FILENAME, scale = 1)
        imageFile = Image.open(self.QRCODE_FILENAME)
        
        
        self.image.paste(imageFile, (x, y))
        
    def show_image(self):
        self.display.image(self.image)
        self.display.display()

    def show_centered_string(self, text, font, x = 0, y = None, lx = None):
        (font_width, font_height) = font.getsize(text)

        lx = lx or (self.display.width)

        img_width = font_width
        img_height = font_height
        img_x = x + (lx-img_width)/2
        img_y = y or (self.display.height-img_height)/2

        draw = ImageDraw.Draw(self.image)
        
        draw.text(
            (img_x, img_y),
            text,
            font=font,
            fill=self.FOREGROUND_COLOR,
        )

    def show_rectangle(self, x, y, lx, ly):
        a = 0
        #draw = ImageDraw.Draw(self.image)
        #draw.fill_rect(x, y, lx, ly, Adafruit_EPD.BLACK)

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


