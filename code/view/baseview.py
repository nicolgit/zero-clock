
class BaseView:

    

    def prepare_image(self): raise NotImplementedError
    def show_image(self): raise NotImplementedError

    def show_centered_string(self, text, font, y = None): raise NotImplementedError     
    def show_welcome(self): raise NotImplementedError



