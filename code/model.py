import time

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