from PySide.QtCore import *

class PunchingBag(QObject):

    punched = Signal()

    def __init__(self):
        super(PunchingBag, self).__init__()

    def punch(self):
        self.punched.emit()


@Slot()
def say_punched():
    print("Bag was punched")



pb = PunchingBag()
pb.punched.connect(say_punched)

for i in range(10):
    pb.punch()
