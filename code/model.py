import time
import socket

class ClockModel(object):
        
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