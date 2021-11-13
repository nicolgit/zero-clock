
from model import ClockModel
from view import ClockView
from controller import ClockController

print("Hello World, I am a clock!")

model = ClockModel()
view = ClockView()
controller = ClockController(model, view)

view.show_welcome()
while True:
    
    controller.show_time()
    controller.sleep()

