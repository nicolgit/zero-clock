import time

class ClockController(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_time(self):
        time = self.model.get_time()
        date = self.model.get_date()

        self.view.prepare_image()
        self.view.show_centered_string(self.model.get_weekday(), self.view.font_medium, 14)
        self.view.show_centered_string(time, self.view.font_huge)
        self.view.show_centered_string(date, self.view.font_medium,90)
        self.view.show_image()

    def sleep(self):
        time.sleep(50)

        
