import time
import digitalio
import board

from enum import Enum
class Pages(Enum):
    Time = 1
    Weather = 2
    Settings = 3

class ClockController(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.up_button = digitalio.DigitalInOut(board.D6)
        self.up_button.switch_to_input()
        self.down_button = digitalio.DigitalInOut(board.D5)
        self.down_button.switch_to_input()

        self.CurrentPage = Pages.Time

    def show_time(self):

        self.view.prepare_image()

        self.view.show_centered_string(self.model.get_weekday(), self.view.font_medium, 0, 0, 140)
        self.view.show_centered_string(self.model.get_time(),    self.view.font_big,    0, 14, 140)
        self.view.show_centered_string(self.model.get_date(),    self.view.font_medium, 0, 44, 140)

        self.view.show_centered_string("----", self.view.font_medium, 180, 0, 50)
        self.view.show_centered_string("T" + self.model.get_weather_temperature(), self.view.font_medium, 180, 18, 50)
        self.view.show_centered_string("H" + self.model.get_weather_humidity(), self.view.font_medium, 180, 36, 50)
        
        self.view.show_rectangle(0,0,50,100)
        
        self.view.show_image()

    def show_weather(self):
        self.view.prepare_image()
        self.view.show_centered_string(self.model.get_weather_place(), self.view.font_medium, 0, 14)
        self.view.show_centered_string(self.model.get_weather_temperature(), self.view.font_huge)
        self.view.show_centered_string(self.model.get_weather_description(), self.view.font_medium, 0, 90)
        self.view.show_image()

    def show_setting(self):
        self.view.prepare_image()
        self.view.show_qrcode(self.model.get_webserver_url(), 1, 1)
        self.view.show_centered_string("settings", self.view.font_medium, 0, 14)
        self.view.show_centered_string(self.model.get_webserver_url(), self.view.font_medium, 0, 32)
        self.view.show_image()

    def sleep(self):
        DURATION = 50
        i=  0

        while (i<DURATION):
            delta = 0.1
            time.sleep(delta)
            i += delta

            if not self.up_button.value:
                if(self.CurrentPage == Pages.Time): 
                    self.CurrentPage = Pages.Weather
                    return
                    
                if(self.CurrentPage == Pages.Weather):
                    self.CurrentPage = Pages.Time
                    return

            if not self.down_button.value:
                if (self.CurrentPage == Pages.Settings): 
                    self.CurrentPage = Pages.Time
                    return
                self.CurrentPage = Pages.Settings
                return
            

            

    def loop(self):
        while True:
            self.model.update_weather_info()

            if (self.CurrentPage == Pages.Time): self.show_time()
            if (self.CurrentPage == Pages.Weather): self.show_weather()
            if (self.CurrentPage == Pages.Settings): self.show_setting()

            self.sleep()

        
