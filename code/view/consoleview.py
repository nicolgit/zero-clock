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

    def show_centered_string(self, text, font, x= None, y = None, lx=None):
        print(text)     
    
    def show_qrcode(self, urlstring, x, y):
        print("QRCODE")
        
    def show_welcome(self):
        print("hello!")