from PySide import QtGui, QtCore
from cdat.Base import BaseOkWindow
from cdat import axis_preview
from cdat.DictEdit import DictEditor
import vcs


class AxisEditorWidget(BaseOkWindow.BaseOkWindowWidget):
    def __init__(self, axis, parent=None):
        super(AxisEditorWidget, self).__init__()
        self.axis = axis
        self.state = None

        # create layout so you can set the preview
        self.horizontal_layout = QtGui.QHBoxLayout()

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

        # set up scrollable for dict editor
        self.scroll_area = QtGui.QScrollArea()
        self.scroll_area.setWidget(self.dict_widget)
        self.scroll_area.setWidgetResizable(True)

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
        preset_box = QtGui.QComboBox()
        preset_box.addItem("default")
        preset_box.addItems(vcs.listelements("list"))
        preset_box.currentIndexChanged[str].connect(self.updatePreset)

        preset_row.addWidget(preset_label)
        preset_row.addWidget(preset_box)

        # create slider for Ticks
        self.ticks_slider = QtGui.QSlider()
        self.ticks_slider.setRange(1, 100)
        self.ticks_slider.setOrientation(QtCore.Qt.Horizontal)
        self.ticks_slider.sliderMoved.connect(self.updateTicks)

        # create step edit box
        step_validator = QtGui.QDoubleValidator()
        self.step_edit = QtGui.QLineEdit()
        self.step_edit.setValidator(step_validator)
        self.step_edit.textEdited.connect(lambda: QtCore.QTimer.singleShot(1000, self.updateStep))
        self.step_edit.editingFinished.connect(self.updateStep)

        # create negative check box
        self.negative_check = QtGui.QCheckBox()
        self.negative_check.clicked.connect(self.updateTickSign)

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

        self.setPreview(axis_preview.AxisPreviewWidget())

    def setPreview(self, preview):
        if self.preview:
            raise Exception("Preview already set")

        self.preview = preview
        self.preview.setMinimumWidth(150)
        self.preview.setMaximumWidth(350)

        if self.axis == "y":
            self.horizontal_layout.insertWidget(0, self.preview)
        elif self.axis == "x":
            self.adjuster_layout.insertWidget(0, self.preview)

    def setAxisObject(self, axis_obj):
        self.object = axis_obj
        self.preview.setAxisObject(self.object)
        self.preview.update()

    # Update mode essentially
    def updateTickmark(self, button):
        if self.axis == "x":
            index = 2
        elif self.axis == "y":
            index = 1
        while self.adjuster_layout.count() > index + 1:
            widget = self.adjuster_layout.takeAt(index).widget()
            widget.setVisible(False)

        if button.text() == "Auto":
            self.adjuster_layout.insertWidget(index, self.preset_widget)
            self.preset_widget.setVisible(True)

        elif button.text() == "Even":
            self.adjuster_layout.insertWidget(index, self.ticks_widget)
            self.ticks_widget.setVisible(True)
            self.state = "count"

        elif button.text() == "Manual":
            self.adjuster_layout.insertWidget(index, self.scroll_area)
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
        self.object.show_miniticks = (state == QtCore.Qt.Checked)
        self.preview.update()

    def updateMiniTicks(self, mini_count):
        self.object.minitick_count = int(mini_count)
        self.preview.update()

    # Update tick count
    def updateTicks(self, value):
        if self.negative_check.checkState() == QtCore.Qt.Checked:
            self.object.numticks = -value
            self.step_edit.setText(str(-self.object.step))
        else:
            self.object.numticks = value
            self.step_edit.setText(str(self.object.step))
        self.state = "count"
        self.preview.update()

    def updateStep(self):
        try:
            cur_val = float(self.step_edit.text())
        except ValueError:
            return

        if cur_val < 0:
            self.negative_check.setCheckState(QtCore.Qt.Checked)
        else:
            self.negative_check.setCheckState(QtCore.Qt.Unchecked)
        self.object.step = cur_val
        self.state = "step"
        self.ticks_slider.setValue(self.object.numticks)

        self.preview.update()

    def updateAxisWithDict(self, dict):
        float_dict = {float(key): value for key, value in dict.items()}
        self.object.ticks = float_dict
        self.preview.update()

    def updateTickSign(self):
        checked = self.negative_check.isChecked()

        # probably a better way of doing this
        if not self.object.numticks:
            self.step_edit.setText(str(self.object.step))
            self.state = "step"

        val = float(self.step_edit.text())

        if self.state == "count":
            value = self.object.numticks
            if checked:
                self.object.numticks = -value
            else:
                self.object.numticks = value

        if self.state == "step":
            self.object.step = str(-val)

        self.step_edit.setText(str(-val))

        self.preview.update()
