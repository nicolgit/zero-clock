import time
import digitalio
import board
import datetime

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

        screen_width   = 250
        screen_height  = 122 

        vlineat = 175
        
        self.view.show_centered_string(self.model.get_weekday(), self.view.font_medium,      0, 0,  vlineat)
        self.view.show_centered_string(self.model.get_time_string(),    self.view.font_huge, 0, 20, vlineat)
        self.view.show_centered_string(self.model.get_date(),    self.view.font_medium,      0, 76, vlineat)
           
        sr = self.model.get_sunrise() # sunrise time
        ss = self.model.get_sunset()  # sunset time
        t = self.model.get_time()     # current time

        remaining = ""
        progress    = 0
        progressmax = 1000
        ss_icon = "A"

        if (t > sr and t < ss):
            progress = (t-sr).total_seconds()
            progressmax = (ss-sr).total_seconds()
            hours, minutes, seconds = self.convert_timedelta (ss - t)
            remaining =  "{}h{}".format(hours, minutes)
            ss_icon = "B"

        if (t > ss):
            progress = (t-ss).total_seconds()
            progressmax = ((sr + datetime.timedelta(days=1)) - ss).total_seconds()
            hours, minutes, seconds = self.convert_timedelta ((sr + datetime.timedelta(days=1)) - t)
            remaining =  "{}h{}".format(hours, minutes)
            ss_icon = "1"
            
        if (t<sr):
            progress = (t - (ss-datetime.timedelta(days=1))).total_seconds()
            progressmax = (sr - (ss - datetime.timedelta(days=1))).total_seconds()
            hours, minutes, seconds = self.convert_timedelta (sr - t)
            remaining =  "{}h{}".format(hours, minutes)
            ss_icon = "1"

        self.view.show_centered_string (self.model.get_weather_temperature(), self.view.font_medium, vlineat, 50, screen_width - vlineat)
        self.view.show_centered_string ("H" + self.model.get_weather_humidity(), self.view.font_medium, vlineat, 74, screen_width - vlineat)
        self.view.draw_icon_and_text (ss_icon, remaining, self.view.font_medium,                        vlineat, 102)

        self.view.draw_line(vlineat, 4, vlineat, 104)

        self.view.draw_weather_icon(self.model.get_weather_icon(), vlineat + 10, 2)
        self.view.draw_progress( 0, 106, vlineat, 10,  progress, progressmax)
        
        self.view.refresh()

    def show_weather(self):
        self.view.prepare_image()
        self.view.show_centered_string(self.model.get_weather_place(), self.view.font_medium, 0, 14)
        self.view.show_centered_string(self.model.get_weather_temperature(), self.view.font_huge)
        self.view.show_centered_string(self.model.get_weather_description(), self.view.font_medium, 0, 90)
        self.view.refresh()

    def show_setting(self):
        self.view.prepare_image()
        self.view.show_qrcode(self.model.get_webserver_url(), 1, 1)
        self.view.show_centered_string("settings", self.view.font_medium, 0, 14)
        self.view.show_centered_string(self.model.get_webserver_url(), self.view.font_medium, 0, 32)
        self.view.refresh()

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
    
    def convert_timedelta(self, duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return hours, minutes, seconds

        
