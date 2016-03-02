from PySide import QtCore, QtGui


class BaseOkWindowWidget(QtGui.QWidget):
    okPressed = QtCore.Signal()

    def __init__(self):
        super(BaseOkWindowWidget, self).__init__()

        self.object = None
        self.preview = None

        # Layout to add new elements
        self.vertical_layout = QtGui.QVBoxLayout()

        # Save and Cancel Buttons
        cancel_button = QtGui.QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(lambda: self.close())

        ok_button = QtGui.QPushButton()
        ok_button.setText("OK")
        ok_button.clicked.connect(self.okClicked)

        ok_cancel_row = QtGui.QHBoxLayout()
        ok_cancel_row.addWidget(cancel_button)
        ok_cancel_row.addWidget(ok_button)
        ok_cancel_row.insertStretch(1, 1)

        # Set up vertical_layout
        self.vertical_layout.addLayout(ok_cancel_row)
        self.setLayout(self.vertical_layout)

    def setPreview(self, preview):
        if self.preview:
            self.vertical_layout.removeWidget(self.preview)
            print "P: ", self.preview
            self.preview.deleteLater()

        self.preview = preview
        self.vertical_layout.insertWidget(0, self.preview)

    def okClicked(self):
        self.okPressed.emit()
        self.close()
