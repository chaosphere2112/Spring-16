from PySide.QtCore import *
from PySide.QtGui import *
from functools import partial
import pdb

class InputChecker(QValidator):

    inputInvalid = Signal()
    correctInput = Signal()

    def __init__(self, index):
        super(InputChecker, self).__init__()
        self.texts = []
        self.index = index

    def validate(self, input, pos):
        if input in self.texts:
            if self.texts.index(input) != self.index:
                self.inputInvalid.emit()
                return QValidator.Intermediate

        self.correctInput.emit()
        return QValidator.Acceptable

    def setIndex(self, index):
        self.index = index


class DictEditor(QWidget):
    dictEdited = Signal(dict)

    def __init__(self):
        super(DictEditor, self).__init__()
        self.valid_keys = None
        self.keys = []
        self.values = []
        self.textEdits = []
        self.valueEdits = []
        self.validators = []
        self.row_count = 0
        self.rows = QVBoxLayout()
        self.button = QVBoxLayout()
        self.wrap = QVBoxLayout()
        add_button = QPushButton()
        add_button.setText("New Line")
        add_button.clicked.connect(self.insertRow)
        self.clearing = False
        self.button.addWidget(add_button)
        self.setLayout(self.wrap)
        self.wrap.addLayout(self.rows)
        self.wrap.addLayout(self.button)

    def colorInvalid(self, line_edit):
        line_edit.setStyleSheet("color: rgb(255, 0, 0);")

    def colorValid(self, line_edit):
        line_edit.setStyleSheet("color: rgb(0, 0, 0);")


    # Update Combo Boxes
    def updateCBoxes(self, cur_box):
        cur_text = cur_box.itemText(cur_box.currentIndex())
        selectedItems = []
        for box in self.cBoxes:
            check_text = box.itemText(box.currentIndex())

            selectedItems.append(check_text)

            # check if boxes match and set to blank if so
            if box != cur_box:
                if check_text == cur_text:
                    box.setCurrentIndex(0)

        return selectedItems


    # updates dict based on lineedit values
    def updateEditTexts(self):
        texts = []
        for item in self.textEdits:
            texts.append(item.text())
        for i in self.validators:
            i.texts = self.keys


    # update lists and selectedItems
    def updateLists(self, left, right, index=None):


        if self.valid_keys:
            selectedItems = self.updateCBoxes(left)
            self.keys = selectedItems
            index = self.keys.index(left.itemText(left.currentIndex()))
            self.values[index] = right.text()


        else:
            key = left.text()
            value = right.text()
            index = self.textEdits.index(left)
            self.keys[index] = key
            self.values[index] = value
            self.updateEditTexts()

        if self.checkKeyValues() and not self.clearing:
            self.dictEdited.emit(dict(zip(self.keys, self.values)))

    # check if valid for emittion
    def checkKeyValues(self):
        text = []
        if self.valid_keys:
            for i in self.cBoxes:
                t = i.itemText(i.currentIndex())
                if t in text or t == "":
                    return False
                text.append(i.itemText(i.currentIndex()))
        else:
            for i in self.textEdits:
                if i.text() in text or i.text() == "":
                    return False
                self.colorValid(i)
                text.append(i.text())

        for i in self.valueEdits:
            if i.text() == "":
                return False
        return True




    # populate if dictionary is given
    def insertRow(self, key="", value=""):

        if self.valid_keys and self.row_count >= len(self.valid_keys)-1:
            return

        self.keys.append(key)
        self.values.append(value)

        # for key, value in self.dict.items():
        col = QHBoxLayout()
        r_button = QPushButton()
        r_button.setText("X")
        r_button.clicked.connect(partial(self.removeRow, col, self.row_count))

        # create right text edit
        edit_right = QLineEdit()
        edit_right.setText(str(value))
        edit_right.setMinimumWidth(100)
        self.valueEdits.append(edit_right)

        if self.valid_keys:
            edit_left = QComboBox()
        else:
            edit_left = QLineEdit()

        listUpdate = partial(self.updateLists, edit_left, edit_right)

        # set text based off if valid_keys has values
        if self.valid_keys:
            for i in self.valid_keys:
                edit_left.addItem(i)
            index = edit_left.findText(str(key))
            if index != -1:
                edit_left.setCurrentIndex(index)

            # assign signals
            edit_left.currentIndexChanged.connect(listUpdate)

            self.cBoxes.append(edit_left)

        else:
            validator = InputChecker(self.row_count)
            self.validators.append(validator)
            edit_left.setValidator(validator)
            validator.correctInput.connect(partial(self.colorValid, edit_left))
            validator.inputInvalid.connect(partial(self.colorInvalid, edit_left))
            edit_left.setText(str(key))

            edit_left.editingFinished.connect(listUpdate)
            self.textEdits.append(edit_left)


        edit_right.editingFinished.connect(listUpdate)
        edit_left.setMinimumWidth(100)
        col.addWidget(r_button)
        col.addWidget(edit_left)
        col.addWidget(edit_right)
        self.rows.addLayout(col)
        self.row_count += 1


    def removeRow(self, section, index):
        child = section.takeAt(0)
        c = 0
        while child:
            widget = child.widget()

            # remove the ComboBox if valid_keys
            if type(widget) == QComboBox:
                self.cBoxes.remove(widget)

            # remove QLineEdit and its Validator. Reindex Validators
            if c == 1 and type(widget) != QComboBox:
                self.validators.remove(self.validators[index])

                for i in range(len(self.validators)):
                    self.validators[i].setIndex(i)
                self.textEdits.remove(widget)

            # Remove the value QLineEdit
            if c == 2:
                self.valueEdits.remove(widget)


            # delete Widget
            child = section.takeAt(0)
            widget.deleteLater()
            c += 1


        # Update Keys and Values
        self.keys.remove(self.keys[index])
        self.values.remove(self.values[index])

        for i in range(self.rows.count()):
            row = self.rows.itemAt(i)
            if row == section:
                self.rows.takeAt(i)
                break
        section.deleteLater()

        self.row_count -= 1

        if self.checkKeyValues() and not self.clearing:
            self.dictEdited.emit(dict(zip(self.keys, self.values)))


    # set valid keys to be selected
    # must call setValidKeys before calling setDict
    def setValidKeys(self, keys):
        self.valid_keys = keys
        self.valid_keys.insert(0, "")
        self.cBoxes = []

    # set inital dictionary values
    def setDict(self, dictionary):

        self.clearing = True

        if len(self.keys) > 0:

            row = self.rows.takeAt(0)
            while row:
                if type(row) == QHBoxLayout:
                    self.removeRow(row, 0)
                row = self.rows.takeAt(0)

        for key, value in dictionary.items():
            self.insertRow(key, value)

        self.clearing = False

        for i in self.validators:
            i.texts = self.keys

    # return valid keys
    def validKeys(self):
        return self.valid_keys

    # return dictionary
    def dict(self):
        return dict(zip(self.keys, self.values))
