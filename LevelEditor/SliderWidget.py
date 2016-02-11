from PySide.QtCore import *
from PySide.QtGui import *
from functools import partial


class AdjustValues(QWidget):
    valuesChanged = Signal(list)

    def __init__(self, parent=None):
        super(AdjustValues, self).__init__(parent=parent)
        self.min_val = 0
        self.max_val = 1
        self.slides = []
        # Insert Sliders
        self.wrap = QVBoxLayout()

        self.rows = []

        # Add Line Button
        self.add_line = QPushButton()
        self.add_line.setText("+ Add Level")
        self.add_line.clicked.connect(self.add_level)
        self.wrap.addWidget(self.add_line)
        self.clearing = False

        # add layout
        self.setLayout(self.wrap)

    def add_level(self):
        self.insert_line()
        if self.clearing is False:
            self.send_values()

    def update(self, minval, maxval, values):
        if minval >= maxval:
            raise ValueError("Minimum value %d >= maximum value %d" % (minval, maxval))
        self.min_val = minval
        self.max_val = maxval
        self.clearing = True
        for ind in range(len(self.rows)):
            self.remove_level(self.rows[0])

        for ind, value in enumerate(values):
            self.insert_line()
            self.slides[ind].setValue(value)
        self.clearing = False

    def adjust_slides(self, slide):
        def call_fb():
            cur_index = self.slides.index(slide)

            for i, s in enumerate(self.slides):

                if i < cur_index:
                    if s.sliderPosition() > slide.sliderPosition():
                        s.setValue(slide.sliderPosition())
                else:
                    if s.sliderPosition() < slide.sliderPosition():
                        s.setValue(slide.sliderPosition())
        return call_fb

    def send_values(self):
        positions = []

        for slide in self.slides:
            positions.append(slide.sliderPosition())
        self.valuesChanged.emit(positions)

    def change_label(self, lab, slide):
        def adj_text():
            lab.setText(str(slide.sliderPosition()))
        return adj_text

    def remove_level(self, row):
        child = row.takeAt(0)
        while child:
            widget = child.widget()

            if type(widget) == QSlider:
                del self.slides[self.slides.index(widget)]

            widget.deleteLater()
            child = row.takeAt(0)
        row.deleteLater()
        self.rows.remove(row)
        if self.clearing is False:
            self.send_values()

    def insert_line(self):
        row = QHBoxLayout()
        lab = QLabel(str(self.max_val))
        slide = QSlider(Qt.Horizontal)

        # remove button
        rem_button = QPushButton()
        rem_button.setText("X")
        rem_button.clicked.connect(partial(self.remove_level, row))

        # populate layout
        row.addWidget(rem_button)
        row.addWidget(lab)
        row.addWidget(slide)

        # set slide attributes
        slide.setRange(self.min_val, self.max_val)
        slide.setValue(self.max_val)
        slide.setTickPosition(QSlider.TicksAbove)
        slide.valueChanged.connect(self.change_label(lab, slide))
        slide.sliderMoved.connect(self.adjust_slides(slide))
        slide.sliderMoved.connect(self.send_values)

        # insert layout
        self.wrap.insertLayout(len(self.slides), row)

        # add to list
        self.slides.append(slide)
        self.rows.append(row)
