import time

class ClockModel(object):
        
    def get_time(self):
        t = time.localtime()
        return time.strftime("%H:%M:%S", t)