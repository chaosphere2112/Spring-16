from PySide import QtCore, QtGui


class BaseWindowWidget(QtGui.QWidget):
    savePressed = QtCore.Signal(str)

    def __init__(self):
        super(BaseWindowWidget, self).__init__()

        self.object = None
        self.preview = None

        # Layout to add new elements
        self.vertical_layout = QtGui.QVBoxLayout()

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

        # Set up vertical_layout
        self.vertical_layout.addLayout(save_cancel_row)
        self.setLayout(self.vertical_layout)

    def setPreview(self, preview):
        if self.preview:
            self.vertical_layout.removeWidget(self.preview)
            print "P: ", self.preview
            self.preview.deleteLater()

        self.preview = preview
        self.vertical_layout.insertWidget(0, self.preview)

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
            self.win.deleteLater()
        except:
            name = self.object.name

        self.savePressed.emit(name)
        self.close()
