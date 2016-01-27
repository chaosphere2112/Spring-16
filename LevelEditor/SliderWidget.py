from PySide.QtCore import *
from PySide.QtGui import *
from collections import OrderedDict

sliders = None


class AdjustValues(QWidget):
    valuesChanged = Signal(list)

    def __init__(self, val_list, min_val, max_val):
        super(AdjustValues, self).__init__()
        self.val_list = val_list
        self.min_val = min_val
        self.max_val = max_val
        self.slider_count = len(val_list)
        self.slides = OrderedDict()

        # Insert Sliders
        self.wrap = QVBoxLayout()

        for i in range(len(val_list)):
            row = QHBoxLayout()
            lab = QLabel(str(val_list[i]))
            slide = QSlider(Qt.Horizontal)

            # remove button
            rem_button = QPushButton()
            rem_button.setText("X")
            rem_button.clicked.connect(self.remove_level(row))

            # setting slider attributes
            slide.setRange(min_val, max_val)
            slide.setTickPosition(QSlider.TicksAbove)
            slide.sliderMoved.connect(self.change_label(lab, slide))
            slide.sliderMoved.connect(self.adjust_slides(slide))
            slide.sliderMoved.connect(self.send_values)
            slide.setValue(val_list[i])

            # label = l, slider = s, position = p

            d = {"l": lab, "s": slide, "p": val_list[i]}

            self.slides[slide] = d
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

    def moved_forward(self, cur_slide):
        keys = self.slides.keys()
        start = None
        for i in keys:
            if i == cur_slide:
                start = keys.index(i)
                break

        for key in self.slides:
            cur = keys.index(key)

            if cur < self.slider_count - 1 and cur >= start:
                next_slide = keys[cur + 1]
                if cur_slide.sliderPosition() > next_slide.sliderPosition():
                    # set values
                    next_slide.setValue(cur_slide.sliderPosition())

                # update dict
                self.slides[cur_slide]["p"] = cur_slide.sliderPosition()
                self.slides[next_slide]["p"] = next_slide.sliderPosition()

                # set labels
                self.slides[cur_slide]["l"].setText(str(cur_slide.sliderPosition()))
                self.slides[next_slide]["l"].setText(str(next_slide.sliderPosition()))
            # your moving the last slide
            else:

                self.slides[cur_slide]["p"] = cur_slide.sliderPosition()
                self.slides[cur_slide]["l"].setText(str(cur_slide.sliderPosition()))

    def moved_backward(self, cur_slide):
        keys = self.slides.keys()
        start = None

        for i in keys:
            if i == cur_slide:
                start = keys.index(i)
                break

        for key in self.slides:
            cur = keys.index(key)

            if cur > 0 and cur <= start:
                prev_slide = keys[cur - 1]
                if cur_slide.sliderPosition() <= prev_slide.sliderPosition():
                    # set values
                    prev_slide.setValue(cur_slide.sliderPosition())
                # update dict
                self.slides[cur_slide]["p"] = cur_slide.sliderPosition()
                self.slides[prev_slide]["p"] = prev_slide.sliderPosition()

                # set labels
                self.slides[cur_slide]["l"].setText(str(cur_slide.sliderPosition()))
                self.slides[prev_slide]["l"].setText(str(prev_slide.sliderPosition()))
            # your moving the first slide
            else:

                self.slides[cur_slide]["p"] = cur_slide.sliderPosition()
                self.slides[cur_slide]["l"].setText(str(cur_slide.sliderPosition()))

    def adjust_slides(self, slide):
        def call_fb():
            if self.slides[slide]["p"] > slide.sliderPosition():
                self.moved_backward(slide)
            else:
                self.moved_forward(slide)

        return call_fb

    def send_values(self):

        label_vals = []

        for val in self.slides.values():
            label_vals.append(val["p"])
        self.valuesChanged.emit(label_vals)

    def change_label(self, lab, slide):
        def adj_text():
            lab.setText(str(slide.sliderPosition()))

        return adj_text

    def remove_level(self, row):
        def perform_remove():

            # remove from dictionary

            child = row.takeAt(0)
            while child:
                widget = child.widget()

                if type(widget) == QSlider:
                    del self.slides[widget]

                widget.deleteLater()
                child = row.takeAt(0)
            row.deleteLater()

            self.slider_count -= 1

        return perform_remove

    def insert_line(self):
        row = QHBoxLayout()
        lab = QLabel(str(self.max_val))
        slide = QSlider(Qt.Horizontal)

        # remove button
        rem_button = QPushButton()
        rem_button.setText("X")

        row.addWidget(rem_button)
        row.addWidget(lab)
        row.addWidget(slide)
        self.wrap.insertLayout(self.slider_count, row)
        self.slider_count += 1
        slide.setRange(self.min_val, self.max_val)
        slide.setValue(self.max_val)
        self.slides[slide] = {"l": lab, "s": slide, "p": self.max_val}
        slide.setTickPosition(QSlider.TicksAbove)
        slide.sliderMoved.connect(self.change_label(lab, slide))
        slide.sliderMoved.connect(self.adjust_slides(slide))
        rem_button.clicked.connect(self.remove_level(row))
