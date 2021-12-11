import json
import os
import datetime
import time
import socket
import requests

class ClockModel(object):

    def __init__(self):

        __location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, "config.json"), "r") as jsonfile:
            CONFIG = json.load(jsonfile)
        jsonfile.close()

        self.weather_api_key = CONFIG["OPEN_WEATHER_API_KEY"]
        self.city = CONFIG["CITY"]

        self.current_weather_time = datetime.datetime(2000, 1, 1, 1, 1, 1)
        self.current_weather = None
        self.update_weather_info()

    def get_time(self):
        t = time.localtime()
        return time.strftime("%H:%M", t)
    
    def get_weekday(self):
        t = time.localtime()
        return time.strftime("%A", t)
    
    def get_month(self):
        t = time.localtime()
        return time.strftime("%B", t)
    
    def get_year(self):
        t = time.localtime()
        return time.strftime("%Y", t)
    
    def get_date(self):
        t = time.localtime()
        return time.strftime("%d %b %Y", t)
    
    def get_webserver_url(self):
        return "http://" + socket.getfqdn() + ":" + str(self.get_webserver_port()) +  "/"
    
    def get_webserver_port(self):
        return 5000
    
    def get_weather_place(self):
        return self.current_weather.get("name") + " " + self.current_weather.get("sys").get("country")

    def get_weather_info(self):
        return self.current_weather.get("weather")[0].get("main")

    def get_weather_description(self):
        return self.current_weather.get("weather")[0].get("description")
    
    def get_weather_temperature(self):
        return str(int(self.current_weather.get("main").get("temp") - 273.15)) + "°C"
    
    def update_weather_info(self):
        c = datetime.datetime.now() - self.current_weather_time
        minutes = c.total_seconds() / 60

        print('Total difference in minutes: ', minutes) 

        if (minutes > 60):
            response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + self.city + "&appid=" + self.weather_api_key)

            weatherjson= response.json()

            self.current_weather_time = datetime.datetime.now()
            self.current_weather = weatherjson

            print (weatherjson.get("coord"))
            print (weatherjson.get("main").get("temp"))


