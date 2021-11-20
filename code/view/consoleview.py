from view.baseview import BaseView

class ConsoleView(BaseView):

    def __init__(self):
        self.font_medium = None
        self.font_big = None
        self.font_huge = None
        
    def prepare_image(self):
        print("")

    def show_image(self): 
        print("")

    def show_centered_string(self, text, font, y = None):
        print(text)     
    
    def show_welcome(self):
        print("hello!")