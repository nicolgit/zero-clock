import time

class ClockController(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_time(self):
        time = self.model.get_time()

        self.view.show_time(time)
    
    def sleep(self):
        time.sleep(10)

        
