from view.baseview import BaseView

import busio
import board
import digitalio
import os
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
        self.FONTSIZE_SMALL = 12
        self.FONTSIZE_MEDIUM = 18
        self.FONTSIZE_BIG = 32
        self.FONTSIZE_HUGE = 52
        self.BACKGROUND_COLOR = WHITE
        self.FOREGROUND_COLOR = BLACK
        self.TEXT_COLOR = BLACK

        self.ICON_MAP = {
            "01d": "B",
            "01n": "C",
            "02d": "H",
            "02n": "I",
            "03d": "N",
            "03n": "N",
            "04d": "Y",
            "04n": "Y",
            "09d": "Q",
            "09n": "Q",
            "10d": "R",
            "10n": "R",
            "11d": "Z",
            "11n": "Z",
            "13d": "W",
            "13n": "W",
            "50d": "J",
            "50n": "K",
        }

        # create the spi device and pins we will need
        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self.ecs = digitalio.DigitalInOut(board.CE0)
        self.dc = digitalio.DigitalInOut(board.D22)
        self.srcs = None
        self.rst = digitalio.DigitalInOut(board.D27)
        self.busy = digitalio.DigitalInOut(board.D17)
        
        current_path = os.path.dirname(__file__)

        print ("current path: " + current_path)

        self.FONT_PATH = current_path + "/../../fonts/DroidSans-Bold.ttf"
        self.font_small = ImageFont.truetype (self.FONT_PATH, self.FONTSIZE_SMALL)
        self.font_medium = ImageFont.truetype(self.FONT_PATH, self.FONTSIZE_MEDIUM)
        self.font_big = ImageFont.truetype   (self.FONT_PATH, self.FONTSIZE_BIG)
        self.font_huge = ImageFont.truetype  (self.FONT_PATH, self.FONTSIZE_HUGE)

        self.font_icons= ImageFont.truetype(current_path + "/../../fonts/meteocons.ttf", 46)
        self.font_icons_small= ImageFont.truetype(current_path + "/../../fonts/meteocons.ttf", 20)

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

    def refresh(self):  
        self.display.image(self.image)
        self.display.display()

    def draw_weather_icon(self, code, x, y):
        draw = ImageDraw.Draw(self.image)
        draw.text(
            (x, y),
            self.ICON_MAP[code],
            font=self.font_icons,
            fill=self.FOREGROUND_COLOR,
        )

    def draw_small_icon(self, text, x, y):
        draw = ImageDraw.Draw(self.image)
        draw.text(
            (x, y),
            text,
            font=self.font_icons_small,
            fill=self.FOREGROUND_COLOR,
        )

    def draw_icon_and_text(self, icon, text, font, x, y):
        (icon_width, icon_height) = self.font_icons_small.getsize(icon)

        draw = ImageDraw.Draw(self.image)
        draw.text((x, y), icon, font=self.font_icons_small, fill=self.FOREGROUND_COLOR)
        draw.text((x+icon_width, y), text, font=font, fill=self.FOREGROUND_COLOR)

    def show_centered_string(self, text, font, x = 0, y = None, lx = None):
        (font_width, font_height) = font.getsize(text)

        if lx is None:
            lx = self.display.width

        img_width = font_width
        img_height = font_height
        img_x = x + (lx-img_width)/2

        if y is None:
            img_y =(self.display.height-img_height)/2
        else:
            img_y = y
        
        draw = ImageDraw.Draw(self.image)
        
        draw.text(
            (img_x, img_y),
            text,
            font=font,
            fill=self.FOREGROUND_COLOR,
        )

    def draw_line(self, x1, y1, x2, y2):
        draw = ImageDraw.Draw(self.image)
        draw.line((x1, y1, x2, y2), fill=self.FOREGROUND_COLOR)

    def draw_progress(self, x, y, lx, ly, current, max):
        draw = ImageDraw.Draw(self.image)
        draw.rectangle((x, y, x+lx, y+ly), fill=None, outline=self.FOREGROUND_COLOR, width=1)
        
        reallx = int(lx * current // max) 
        draw.rectangle((x, y, x+reallx, y+ly), fill=self.FOREGROUND_COLOR)
        
        triangle_width = x + reallx + 6
        if triangle_width > x+lx:
            triangle_width = x+lx

        triangle = [(x+reallx,y), (x+reallx,y+ly), (triangle_width,y+ly), (x+reallx,y)] 
        draw.polygon(triangle, fill=self.FOREGROUND_COLOR)


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


