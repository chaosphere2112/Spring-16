from PySide.QtCore import *
from PySide.QtGui import *


class InputChecker(QValidator):

    inputInvalid = Signal()
    correctInput = Signal()

    def __init__(self, index):
        super(InputChecker, self).__init__()
        self.texts = []
        self.index = index

    def validate(self, input, pos):
        print input, self.texts, self.index
        if input in self.texts:
            if self.texts.index(input) != self.index:
                self.inputInvalid.emit()
                return QValidator.Intermediate

        self.correctInput.emit()
        return QValidator.Acceptable

    def setIndex(self, index):
        self.index = index


class DictEditor(QWidget):
    textEdited = Signal(dict)

    def __init__(self):
        super(DictEditor, self).__init__()
        self.valid_keys = None
        # self.dict = OrderedDict()
        self.keys = []
        self.values = []
        self.textEdits = []
        self.validators = []
        self.row_count = 0
        self.rows = QVBoxLayout()
        add_button = QPushButton()
        add_button.setText("New Line")
        add_button.clicked.connect(self.insertRow)

        self.rows.addWidget(add_button)
        self.setLayout(self.rows)

    def colorInvalid(self, line_edit):
        def applyColor():
            line_edit.setStyleSheet("color: rgb(255, 0, 0);")
        return applyColor

    def colorValid(self, line_edit):
        def applyColor():
            line_edit.setStyleSheet("color: rgb(0, 0, 0);")
        return applyColor


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
        '''
        for key in self.dict.keys():
            if key not in texts:
                del self.dict[key]
        '''
        for i in self.validators:
            i.texts = self.keys


    # update dictionary and selectedItems
    def updateLists(self, left, right, index):

        def applyUpdate():
            if self.valid_keys:
                key = left.itemText(left.currentIndex())
                selectedItems = self.updateCBoxes(left)
                if key:
                    print "apply update", key
                    print "SI: ", self.selectedItems
                    self.dict[key] = right.text()

                    # remove unused values from dict
                    for key in self.dict.keys():
                        print "K:", key
                        if key not in selectedItems:
                            print "Deleting", key
                            del self.dict[key]
            else:
                key = left.text()
                value = right.text()
                # self.dict[key] = right.text()
                self.keys[index] = key
                self.values[index] = value
                self.updateEditTexts()

            self.textEdited.emit(dict(zip(self.keys, self.values)))

        return applyUpdate



    # populate if dictionary is given
    # def populateView(self):

    def insertRow(self, key="", value=""):

        self.keys.append(key)
        self.values.append(value)

        # for key, value in self.dict.items():
        col = QHBoxLayout()
        r_button = QPushButton()
        r_button.setText("X")
        r_button.clicked.connect(self.removeRow(col, self.row_count))

        # create right text edit
        edit_right = QLineEdit()
        edit_right.setText(str(value))
        edit_right.setMinimumWidth(100)

        # set text based off if valid_keys has values
        if self.valid_keys:
            edit_left = QComboBox()
            for i in self.valid_keys:
                edit_left.addItem(i)
            index = edit_left.findText(str(key))
            if index != -1:
                edit_left.setCurrentIndex(index)

            # assign signals
            edit_left.currentIndexChanged.connect(self.updateLists(edit_left, edit_right, self.row_count))

            self.cBoxes.append(edit_left)

        else:
            edit_left = QLineEdit()
            validator = InputChecker(self.row_count)
            self.validators.append(validator)
            edit_left.setValidator(validator)
            validator.correctInput.connect(self.colorValid(edit_left))
            validator.inputInvalid.connect(self.colorInvalid(edit_left))

            edit_left.setText(str(key))
            edit_left.editingFinished.connect(self.updateLists(edit_left, edit_right, self.row_count))
            self.textEdits.append(edit_left)

        edit_right.editingFinished.connect(self.updateLists(edit_left, edit_right, self.row_count))
        edit_left.setMinimumWidth(100)
        col.addWidget(r_button)
        col.addWidget(edit_left)
        col.addWidget(edit_right)
        self.rows.insertLayout(self.row_count, col)
        self.row_count += 1


        '''
        def insertRow(self, key="", value=""):

        col = QHBoxLayout()
        r_button = QPushButton()
        r_button.setText("X")
        r_button.clicked.connect(self.removeRow(col, self.row_count))

        edit_right = QLineEdit()

        if self.valid_keys:
            edit_left = QComboBox()
            for i in self.valid_keys:
                edit_left.addItem(i)
            self.cBoxes.append(edit_left)
            edit_left.currentIndexChanged.connect(self.updateDict(edit_left, edit_right))

        else:
            edit_left = QLineEdit()
            validator = InputChecker(self.row_count)
            self.validators.append(validator)
            edit_left.setValidator(validator)
            validator.correctInput.connect(self.colorValid(edit_left))
            validator.inputInvalid.connect(self.colorInvalid(edit_left))

            edit_left.editingFinished.connect(self.updateDict(edit_left, edit_right))
            self.textEdits.append(edit_left)

        edit_left.setMinimumWidth(100)
        edit_right.setMinimumWidth(100)
        edit_right.editingFinished.connect(self.updateDict(edit_left, edit_right))

        col.addWidget(r_button)
        col.addWidget(edit_left)
        col.addWidget(edit_right)

        self.rows.insertLayout(self.row_count, col)
        self.row_count += 1
        '''


    def removeRow(self, section, index):
        def performRemove():

            child = section.takeAt(0)
            c = 0
            while child:
                widget = child.widget()
                if type(widget) == QComboBox:
                    self.cBoxes.remove(widget)

                if c == 1 and type(widget) != QComboBox:
                    self.validators.remove(self.validators[index])
                    for i in range(len(self.validators)):
                        print len(self.validators), i, index

                        self.validators[i].setIndex(i)

                    self.keys.remove(self.keys[index])
                    self.values.remove(self.values[index])
                    print widget.text()


                widget.deleteLater()
                child = section.takeAt(0)
                c += 1
            section.deleteLater()
            self.row_count -= 1

            self.textEdited.emit(dict(zip(self.keys, self.values)))

        return performRemove


    # set valid keys to be selected
    def setValidKeys(self, keys):
        self.valid_keys = keys
        self.valid_keys.insert(0, "")
        self.cBoxes = []

    # set inital dictionary values
    def setDict(self, dictionary):
        # self.populateView()
        for key, value in dictionary.items():
            self.insertRow(key, value)
        for i in self.validators:
            i.texts = self.keys


    # return valid keys
    def validKeys(self):
        return self.valid_keys

    # return dictionary
    def dict(self):
        return self.dict
