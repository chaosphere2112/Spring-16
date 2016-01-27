from PySide.QtCore import *
from PySide.QtGui import *
from collections import OrderedDict

sliders = None


class AdjustValues(QWidget):
    valuesChanged = Signal(list)

    def __init__(self, val_list, min_val, max_val):
        super(AdjustValues, self).__init__()
        self.min_val = min_val
        self.max_val = max_val
        self.slides = []

        # Insert Sliders
        self.wrap = QVBoxLayout()

        for value in val_list:
            row = QHBoxLayout()
            lab = QLabel(str(value))
            slide = QSlider(Qt.Horizontal)

            # remove button
            rem_button = QPushButton()
            rem_button.setText("X")
            rem_button.clicked.connect(self.remove_level(row))

            # setting slider attributes
            slide.setRange(min_val, max_val)
            slide.setTickPosition(QSlider.TicksAbove)
            slide.valueChanged.connect(self.change_label(lab, slide))
            slide.sliderMoved.connect(self.adjust_slides(slide))
            slide.sliderMoved.connect(self.send_values)
            slide.setValue(value)

            # add to list
            self.slides.append(slide)

            # create row and add row
            row.addWidget(rem_button)
            row.addWidget(lab)
            row.addWidget(slide)
            self.wrap.addLayout(row)

        # Add Line Button
        self.add_line = QPushButton()
        self.add_line.setText("+ Add Level")
        self.add_line.clicked.connect(self.insert_line)
        self.wrap.addWidget(self.add_line)

        # add layout
        self.setLayout(self.wrap)

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
        def perform_remove():

            child = row.takeAt(0)
            while child:
                widget = child.widget()

                if type(widget) == QSlider:
                    del self.slides[self.slides.index(widget)]

                widget.deleteLater()
                child = row.takeAt(0)
            row.deleteLater()

        return perform_remove

    def insert_line(self):
        row = QHBoxLayout()
        lab = QLabel(str(self.max_val))
        slide = QSlider(Qt.Horizontal)

        # remove button
        rem_button = QPushButton()
        rem_button.setText("X")
        rem_button.clicked.connect(self.remove_level(row))

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
