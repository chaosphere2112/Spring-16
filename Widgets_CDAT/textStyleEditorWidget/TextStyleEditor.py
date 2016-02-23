import vcs
import text_style_preview
from PySide import QtCore, QtGui


class TextStyleEditor(QtGui.QWidget):

    savePressed = QtCore.Signal(str)
    
    def __init__(self):
        super(TextStyleEditor, self).__init__()
        self.textObject = None

        wrap = QtGui.QVBoxLayout()

        # Set up vertical align
        self.va_group = QtGui.QButtonGroup()
        va_layout = QtGui.QHBoxLayout()

        for alignment in ["Top", "Mid", "Bot"]:

            button = QtGui.QPushButton()
            button.setText(alignment)
            button.setCheckable(True)
            va_layout.addWidget(button)
            self.va_group.addButton(button)

        self.va_group.buttonClicked.connect(self.updateButton)

        va_box = QtGui.QGroupBox()
        va_box.setLayout(va_layout)
        va_box.setTitle("Vertical Align")

        # Set up horizontal group
        self.ha_group = QtGui.QButtonGroup()
        ha_layout = QtGui.QHBoxLayout()

        for alignment in ["Left", "Center", "Right"]:
            button = QtGui.QPushButton()
            button.setText(alignment)
            button.setCheckable(True)
            ha_layout.addWidget(button)
            self.ha_group.addButton(button)

        self.ha_group.buttonClicked.connect(self.updateButton)

        ha_box = QtGui.QGroupBox()
        ha_box.setLayout(ha_layout)
        ha_box.setTitle("Horizontal Align")

        # First row
        align_angle_row = QtGui.QHBoxLayout()
        align_angle_row.addWidget(va_box)
        align_angle_row.addWidget(ha_box)
        align_angle_row.insertStretch(2, 1)

        # Preview setup
        self.preview = text_style_preview.TextStylePreviewWidget()

        # Create labels
        angle_label = QtGui.QLabel()
        angle_label.setText("Angle:")
        font_label = QtGui.QLabel()
        font_label.setText("Font:")
        size_label = QtGui.QLabel()
        size_label.setText("Size:")

        # angle dial setup
        self.angle_slider = QtGui.QDial()
        self.angle_slider.setRange(90, 450)  # set rotate values so dial orientation matches initial text
        self.angle_slider.setWrapping(True)
        self.angle_slider.setNotchesVisible(True)
        self.angle_slider.valueChanged.connect(self.updateAngle)

        align_angle_row.addWidget(angle_label)
        align_angle_row.addWidget(self.angle_slider)

        # Font combobox
        self.font_box = QtGui.QComboBox()
        for item in vcs.listelements("font"):
            self.font_box.addItem(item)
        self.font_box.currentIndexChanged[str].connect(self.updateFont)

        # size spin box
        self.size_box = QtGui.QSpinBox()
        self.size_box.setRange(1, 128)
        self.size_box.valueChanged.connect(self.updateSize)


        font_size_row = QtGui.QHBoxLayout()
        font_size_row.addWidget(font_label)
        font_size_row.addWidget(self.font_box)
        font_size_row.addWidget(size_label)
        font_size_row.addWidget(self.size_box)
        font_size_row.insertStretch(2, 3)

        # Save and Cancel Buttons

        cancel_button = QtGui.QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(lambda: self.close())

        saveas_button = QtGui.QPushButton()
        saveas_button.setText("Save As")
        saveas_button.clicked.connect(self.saveAs)

        save_button = QtGui.QPushButton()
        save_button.setText("Save")
        save_button.clicked.connect(self.save)

        save_cancel_row = QtGui.QHBoxLayout()
        save_cancel_row.addWidget(cancel_button)
        save_cancel_row.addWidget(saveas_button)
        save_cancel_row.addWidget(save_button)
        save_cancel_row.insertStretch(1, 1)

        # Set up wrap
        wrap.addWidget(self.preview)
        wrap.addLayout(align_angle_row)
        wrap.addLayout(font_size_row)
        wrap.addLayout(save_cancel_row)
        self.setLayout(wrap)


    def setTextObject(self, text_object):
        self.textObject = text_object
        self.preview.setTextObject(self.textObject)
        self.setWindowTitle('Edit Style "%s"' % self.textObject.name)

        # set initial values
        cur_valign = self.textObject.valign
        for button in self.va_group.buttons():
            if cur_valign == 0 and button.text() == "Top":
                button.setChecked(True)
            elif cur_valign == 2 and button.text() == "Mid":
                button.setChecked(True)
            elif cur_valign == 4 and button.text() == "Bot":
                button.setChecked(True)

        cur_halign = self.textObject.halign
        for button in self.ha_group.buttons():
            if cur_halign == 0 and button.text() == "Left":
                button.setChecked(True)
            elif cur_halign == 1 and button.text() == "Center":
                button.setChecked(True)
            elif cur_halign == 2 and button.text() == "Right":
                button.setChecked(True)

        self.angle_slider.setSliderPosition(self.textObject.angle)

        self.size_box.setValue(self.textObject.height)


    def updateButton(self, button):
        if button.text() == "Top":
            self.textObject.valign = "top"

        elif button.text() == "Mid":
            self.textObject.valign = "half"

        elif button.text() == "Bot":
            self.textObject.valign = "bottom"

        elif button.text() == "Left":
            self.textObject.halign = "left"

        elif button.text() == "Center":
            self.textObject.halign = "center"

        elif button.text() == "Right":
            self.textObject.halign = "right"

        self.preview.update()

    def updateAngle(self, angle):

        self.textObject.angle = angle % 360  # angle cannot be higher than 360

        self.preview.update()


    def updateFont(self, font):

        self.textObject.font = str(font)

        self.preview.update()

    def updateSize(self, size):

        self.textObject.height = size

        self.preview.update()

    def saveAs(self):

        self.win = QtGui.QInputDialog()

        self.win.setLabelText("Enter New Name:")
        self.win.accepted.connect(self.save)

        self.win.show()
        self.win.raise_()


    def save(self):

        try:
            name = self.win.textValue()
            self.win.close()
        except:
            name = self.textObject.name

        self.savePressed.emit(name)
        self.close()
