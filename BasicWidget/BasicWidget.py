import sys

from PySide.QtCore import *
from PySide.QtGui import *


qt_app = QApplication(sys.argv)
"""widget = QWidget()
widget.setWindowTitle('I Am A Window')
widget.setMinimumSize(QSize(500,500))

label = QLabel('Hello, world!', widget)
label.setAlignment(Qt.AlignRight)

label.show()
widget.show()

qt_app.exec_()"""

class HelloWorldApp(QLabel):

    def __init__(self):
        QLabel.__init__(self,"Hello World")

        self.setMinimumSize(QSize(500,500))
        self.setAlignment(Qt.AlignCenter)
        self.setWindowTitle('Hello World')

    def run(self):

        self.show()
        qt_app.exec_()

HelloWorldApp().run()
