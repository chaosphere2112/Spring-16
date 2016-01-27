from PySide.QtCore import *
from PySide.QtGui import *
import SliderWidget


def print_vals(vals):
    SliderWidget.sliders.close()
    for v in vals:
        print(v)


if __name__ == '__main__':
    app = QApplication([])

    l = [0, 20, 40, 60, 80, 100]
    min = 0
    max = 100

    SliderWidget.launch_adjuster(l, min, max)
    SliderWidget.sliders.values.connect(print_vals)

    app.exec_()
