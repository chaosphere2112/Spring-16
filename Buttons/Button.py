import sys
from PySide.QtCore import Slot
from PySide.QtGui import *

app = QApplication(sys.argv)

win = QWidget()
win.setWindowTitle('TestWindow')

btn = QPushButton('Test', win)

@Slot()
def on_click():
    print("Clicked")

@Slot()
def on_press():
    print("Pressed")

@Slot()
def on_release():
    print("Released")

btn.clicked.connect(on_click)
btn.pressed.connect(on_press)
btn.released.connect(on_release)

win.show()
app.exec_()
