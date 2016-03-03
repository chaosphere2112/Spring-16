from PySide import QtGui, QtCore
from cdat.Base import BaseOkWindow
from cdat.XAxisEdit import axis_preview
from cdat.DictEdit import DictEditor
import vcs


class XAxisEditorWidget(BaseOkWindow.BaseOkWindowWidget):
    def __init__(self, axis):
        super(XAxisEditorWidget, self).__init__()
        self.setPreview(axis_preview.AxisPreviewWidget(axis))
        self.object = axis

        # create labels
        tickmarks_label = QtGui.QLabel("Tickmarks:")
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
        preset_box = QtGui.QComboBox()
        preset_box.addItem("default")
        preset_box.addItems(vcs.listelements("list"))
        preset_box.currentIndexChanged[str].connect(self.updatePreset)

        preset_row.addWidget(preset_label)
        preset_row.addWidget(preset_box)

        # create slider for Ticks
        ticks_slider = QtGui.QSlider()
        ticks_slider.setRange(1, 100)
        ticks_slider.setOrientation(QtCore.Qt.Horizontal)
        ticks_slider.valueChanged.connect(self.updateTicks)

        self.step_edit = QtGui.QLineEdit()
        self.step_edit.editingFinished.connect(self.updateStep)

        ticks_row.addWidget(ticks_label)
        ticks_row.addWidget(ticks_slider)
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

        self.vertical_layout.insertLayout(1, tickmarks_row)
        self.vertical_layout.insertWidget(2, self.preset_widget)
        self.vertical_layout.insertLayout(3, mini_ticks_row)

    def setAxisObject(self, axis_obj):
        self.object = axis_obj
        self.preview.setAxisObject(self.object)

    def updateTickmark(self, button):
        while self.vertical_layout.count() > 4:
            widget = self.vertical_layout.takeAt(2).widget()
            widget.setVisible(False)

        if button.text() == "Auto":
            self.vertical_layout.insertWidget(2, self.preset_widget)
            self.preset_widget.setVisible(True)
        elif button.text() == "Even":
            self.vertical_layout.insertWidget(2, self.ticks_widget)
            self.ticks_widget.setVisible(True)
        elif button.text() == "Manual":
            self.vertical_layout.insertWidget(2, self.dict_widget)
            self.dict_widget.setVisible(True)

        self.object.mode = button.text().lower()
        self.preview.update()

    def updatePreset(self, preset):
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
        self.object.numticks = value
        self.preview.update()

    def updateStep(self):
        self.object.step = self.step_edit.text()
        self.preview.update()

