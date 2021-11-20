
from model import ClockModel
model = ClockModel()

from view.einkview import EinkView
view = EinkView()

#from view.consoleview import ConsoleView
#view = ConsoleView()

view.show_welcome()

from controller import ClockController
controller = ClockController(model, view)

controller.loop()
