from PySide import QtGui, QtCore
from cdat.Base import BaseOkWindow
from cdat import axis_preview
from cdat.DictEdit import DictEditor
import vcs


class YAxisEditorWidget(BaseOkWindow.BaseOkWindowWidget):
    def __init__(self, parent=None):
        super(YAxisEditorWidget, self).__init__()

        # create layout so you can set the preview
        self.horizontal_layout = QtGui.QHBoxLayout()
        self.setPreview(axis_preview.AxisPreviewWidget())
        self.state = None

        # create labels
        tickmarks_label = QtGui.QLabel("Tickmarks:")
        negative_label = QtGui.QLabel("Negative:")
        ticks_label = QtGui.QLabel("Ticks:")
        step_label = QtGui.QLabel("Tick Step:")
        show_mini_label = QtGui.QLabel("Show Mini Ticks:")
        mini_per_tick_label = QtGui.QLabel("Mini-Ticks Per Tick:")
        preset_label = QtGui.QLabel("Preset:")

        # create rows
        tickmarks_row = QtGui.QHBoxLayout()
        preset_row = QtGui.QHBoxLayout()
        ticks_row = QtGui.QHBoxLayout()
        mini_ticks_row = QtGui.QHBoxLayout()

        # create widgets
        self.ticks_widget = QtGui.QWidget()
        self.ticks_widget.setLayout(ticks_row)
        self.preset_widget = QtGui.QWidget()
        self.preset_widget.setLayout(preset_row)
        self.dict_widget = DictEditor.DictEditorWidget()
        self.dict_widget.dictEdited.connect(self.updateAxisWithDict)

        # Create radio buttons and group them
        self.tickmark_button_group = QtGui.QButtonGroup()
        tickmarks_row.addWidget(tickmarks_label)

        for name in ["Auto", "Even", "Manual"]:
            button = QtGui.QRadioButton(name)
            tickmarks_row.addWidget(button)
            if name == "Auto":
                button.setChecked(True)
            self.tickmark_button_group.addButton(button)

        self.tickmark_button_group.buttonClicked.connect(self.updateTickmark)

        # create preset combo box
        # This in only being tracked for debugging
        self.preset_box = QtGui.QComboBox()
        self.preset_box.addItem("default")
        self.preset_box.addItems(vcs.listelements("list"))
        self.preset_box.currentIndexChanged[str].connect(self.updatePreset)

        preset_row.addWidget(preset_label)
        preset_row.addWidget(self.preset_box)

        # create slider for Ticks
        self.ticks_slider = QtGui.QSlider()
        self.ticks_slider.setRange(1, 100)
        self.ticks_slider.setOrientation(QtCore.Qt.Horizontal)
        self.ticks_slider.sliderMoved.connect(self.updateTicks)

        # create step edit box

        step_validator = QtGui.QDoubleValidator()
        step_validator.setBottom(1)
        self.step_edit = QtGui.QLineEdit()
        self.step_edit.setValidator(step_validator)
        self.step_edit.textEdited.connect(lambda: QtCore.QTimer.singleShot(2000, self.updateStep))
        self.step_edit.editingFinished.connect(self.updateStep)

        # create negative check box
        self.negative_check = QtGui.QCheckBox()
        self.negative_check.stateChanged.connect(self.updateTickSign)

        ticks_row.addWidget(negative_label)
        ticks_row.addWidget(self.negative_check)
        ticks_row.addWidget(ticks_label)
        ticks_row.addWidget(self.ticks_slider)
        ticks_row.addWidget(step_label)
        ticks_row.addWidget(self.step_edit)

        # create show mini ticks check box
        show_mini_check_box = QtGui.QCheckBox()
        show_mini_check_box.stateChanged.connect(self.updateShowMiniTicks)

        # create mini tick spin box
        mini_tick_box = QtGui.QSpinBox()
        mini_tick_box.setRange(0, 255)
        mini_tick_box.valueChanged.connect(self.updateMiniTicks)

        mini_ticks_row.addWidget(show_mini_label)
        mini_ticks_row.addWidget(show_mini_check_box)
        mini_ticks_row.addWidget(mini_per_tick_label)
        mini_ticks_row.addWidget(mini_tick_box)

        self.adjuster_layout = QtGui.QVBoxLayout()

        self.adjuster_layout.insertLayout(0, tickmarks_row)
        self.adjuster_layout.insertWidget(1, self.preset_widget)
        self.adjuster_layout.insertLayout(2, mini_ticks_row)

        self.horizontal_layout.addLayout(self.adjuster_layout)

        self.vertical_layout.insertLayout(0, self.horizontal_layout)

    def setPreview(self, preview):
        if self.preview:
            self.horizontal_layout.removeWidget(self.preview)
            self.preview.deleteLater()

        self.preview = preview
        self.horizontal_layout.insertWidget(0, self.preview)

    def setAxisObject(self, axis_obj):
        print "setting axis object"
        self.object = axis_obj
        self.preview.setAxisObject(self.object)
        self.preview.update()

    def updateTickmark(self, button):
        while self.adjuster_layout.count() > 2:
            widget = self.adjuster_layout.takeAt(1).widget()
            widget.setVisible(False)

        if button.text() == "Auto":
            self.adjuster_layout.insertWidget(1, self.preset_widget)

            print self.preset_box.currentText(), self.preset_box.currentIndex()
            self.preset_widget.setVisible(True)
        elif button.text() == "Even":
            self.adjuster_layout.insertWidget(1, self.ticks_widget)
            self.ticks_widget.setVisible(True)
            self.state = "count"
        elif button.text() == "Manual":
            self.adjuster_layout.insertWidget(1, self.dict_widget)
            print "TICKS AS DICT:", self.object.ticks_as_dict()
            self.dict_widget.setDict(self.object.ticks_as_dict())
            self.dict_widget.setVisible(True)

        self.object.mode = button.text().lower()
        self.preview.update()

    def updatePreset(self, preset):
        if preset == "default":
            self.object.ticks = "*"
        else:
            self.object.ticks = preset
        self.preview.update()

    def updateShowMiniTicks(self, state):
        if state == QtCore.Qt.Checked:
            self.object.show_miniticks = True
        elif state == QtCore.Qt.Unchecked:
            self.object.show_miniticks = False
        self.preview.update()

    def updateMiniTicks(self, mini_count):
        self.object.minitick_count = int(mini_count)
        self.preview.update()

    def updateTicks(self, value):

        if self.negative_check.checkState() == QtCore.Qt.Checked:
            self.object.numticks = -value
        else:
            self.object.numticks = value
        self.state = "count"
        self.preview.update()
        self.step_edit.setText(str(self.object.step))

    def updateStep(self):
        print "updating step"
        cur_val = self.step_edit.text()
        if self.negative_check.checkState() == QtCore.Qt.Checked:
            cur_val = str(-float(cur_val))
        self.object.step = cur_val
        self.state = "step"
        self.preview.update()
        self.ticks_slider.setValue(self.object.numticks)

    def updateAxisWithDict(self, dict):
        float_dict = {float(key): value for key, value in dict.items()}
        self.object.ticks = float_dict
        self.preview.update()

    def updateTickSign(self, state):
        if state == QtCore.Qt.Checked:
            if self.state == "count":
                value = self.object.numticks
                self.object.numticks = -value
            elif self.state == "step":
                neg_val = -float(self.step_edit.text())
                self.step_edit.setText(str(abs(neg_val)))
                self.object.step = str(neg_val)
        else:
            if self.state == "count":
                value = self.object.numticks
                self.object.numticks = value
            elif self.state == "step":
                pos_val = abs(float(self.step_edit.text()))
                pos_val = str(pos_val)
                self.object.step = pos_val
                self.step_edit.setText(pos_val)

        self.preview.update()
