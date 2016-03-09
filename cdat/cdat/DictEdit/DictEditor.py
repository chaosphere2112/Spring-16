from PySide.QtCore import *
from PySide.QtGui import *
from functools import partial


class KeyValueRow(QWidget):
    clickedRemove = Signal(QWidget)
    updatedKey = Signal(QWidget)
    updatedValue = Signal(QWidget)

    def __init__(self, key="", value="", valid_keys=None, parent=None):
        super(KeyValueRow, self).__init__(parent=parent)
        wrap = QHBoxLayout()
        self.valid_keys = valid_keys
        self.setMinimumHeight(40)

        if valid_keys:
            self.edit_key = QComboBox()
        else:
            self.edit_key = QLineEdit()

        self.edit_value = QLineEdit()

        if self.valid_keys:
            for i in self.valid_keys:
                self.edit_key.addItem(i)
            index = self.edit_key.findText(str(key))
            if index != -1:
                self.edit_key.setCurrentIndex(index)

            # assign signals
            self.edit_key.currentIndexChanged.connect(lambda: self.updatedKey.emit(self))

        else:
            self.edit_key.setText(str(key))
            self.edit_key.editingFinished.connect(lambda: self.updatedKey.emit(self))
            self.edit_key.setMinimumWidth(100)

        self.edit_value.setText(str(value))
        self.edit_value.setMinimumWidth(100)
        self.edit_value.editingFinished.connect(lambda: self.updatedValue.emit(self))

        r_button = QPushButton()
        r_button.setText("X")
        r_button.clicked.connect(lambda: self.clickedRemove.emit(self))

        wrap.addWidget(r_button)
        wrap.addWidget(self.edit_key)
        wrap.addWidget(self.edit_value)
        self.setLayout(wrap)

    def setValid(self, is_valid):
        if is_valid:
            self.edit_key.setStyleSheet("color: rgb(0, 0, 0);")
        else:
            self.edit_key.setStyleSheet("color: rgb(255, 0, 0);")

    def setKeyValidator(self, validator):
        self.edit_key.setValidator(validator)
        validator.correctInput.connect(partial(self.setValid, True))
        validator.inputInvalid.connect(partial(self.setValid, False))

    def key(self):
        if isinstance(self.edit_key, QLineEdit):
            return self.edit_key.text()
        else:
            return self.edit_key.itemText(self.edit_key.currentIndex())

    def value(self):
        return self.edit_value.text()

    def setKey(self, text):
        if self.valid_keys:
            index = self.edit_key.findText(str(text))
            if index != -1:
                self.edit_key.setCurrentIndex(index)
        else:
            self.edit_key.setText(text)

    def setValue(self, text):
        self.edit_value.setText(text)


class InputChecker(QValidator):
    inputInvalid = Signal()
    correctInput = Signal()

    def __init__(self, index, editor):
        super(InputChecker, self).__init__()
        self.editor = editor
        self.index = index

    def validate(self, input, pos):
        keys = []
        for index, row in enumerate(self.editor.key_value_rows):
            if index != self.index:
                keys.append(row.key())

        if input in keys:
            self.inputInvalid.emit()
            return QValidator.Intermediate

        self.correctInput.emit()
        return QValidator.Acceptable


class DictEditorWidget(QWidget):
    dictEdited = Signal(dict)

    def __init__(self):
        super(DictEditorWidget, self).__init__()
        self.valid_keys = None
        self.key_value_rows = []
        self.rows = QVBoxLayout()
        self.clearing = False

        wrap = QVBoxLayout()
        add_button = QPushButton()
        add_button.setText("New Line")
        add_button.clicked.connect(self.insertRow)

        self.setLayout(wrap)
        wrap.addLayout(self.rows)
        wrap.addWidget(add_button)

    # Update Combo Boxes
    def updateCBoxes(self, cur_row):
        cur_text = cur_row.key()

        for row in self.key_value_rows:
            check_text = row.key()
            # check if boxes match and set to blank if so
            if row != cur_row:
                if check_text == cur_text:
                    # accessing edit_key here
                    row.edit_key.setCurrentIndex(0)

    # check if valid for emission
    def checkKeyValues(self):
        keys = []
        values = []
        for row in self.key_value_rows:
            l_text = row.key()
            r_text = row.value()
            if l_text and l_text not in keys:
                keys.append(l_text)
                values.append(r_text)
        return (keys, values)

    def emitSignal(self):
        keys, values = self.checkKeyValues()
        if keys and values:
            self.dictEdited.emit(dict(zip(keys, values)))

    # populate if dictionary is given
    def insertRow(self, key="", value=""):
        if self.valid_keys and self.rows.count() >= len(self.valid_keys) - 1:
            return

        new_row = KeyValueRow(key, value, self.valid_keys, self)
        new_row.updatedKey.connect(self.emitSignal)
        new_row.updatedValue.connect(self.emitSignal)
        new_row.clickedRemove.connect(self.removeRow)

        if not self.valid_keys:
            validator = InputChecker(self.rows.count(), self)
            new_row.setKeyValidator(validator)
        if self.valid_keys:
            new_row.updatedKey.connect(self.updateCBoxes)

        self.rows.addWidget(new_row)
        self.key_value_rows.append(new_row)

    def removeRow(self, row_widget):
        layout = row_widget.layout()
        child = layout.takeAt(0)

        while child:
            widget = child.widget()
            child = layout.takeAt(0)
            widget.deleteLater()

        # Remove from list
        self.key_value_rows.remove(row_widget)

        layout.deleteLater()
        row_widget.deleteLater()

        if not self.clearing:
            self.emitSignal()

    # set valid keys to be selected
    # must call setValidKeys before calling setDict
    def setValidKeys(self, keys):
        self.valid_keys = keys
        self.valid_keys.insert(0, "")

    # set inital dictionary values
    def setDict(self, dictionary):

        self.clearing = True
        if self.rows.count() > 0:
            row = self.rows.takeAt(0)

            while row:
                row_widget = row.widget()
                self.removeRow(row_widget)
                row = self.rows.takeAt(0)

        for key in sorted(dictionary.keys()):
            self.insertRow(key, dictionary[key])

        self.clearing = False

    # return valid keys
    def validKeys(self):
        return self.valid_keys

    # return dictionary
    def dict(self):
        keys = []
        values = []
        for row in self.key_value_rows:
            keys.append(row.key())
            values.append(row.value())
        return dict(zip(keys, values))
