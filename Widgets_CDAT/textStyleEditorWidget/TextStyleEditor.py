import vcs
import cdms2
from PySide import QtCore, QtGui

class TextStyleEditor(QtGui.QWidget):
    
    def __init__(self):
        super(TextStyleEditor, self).__init__()
        self.textObject = None
        wrap = QtGui.QVBoxLayout()

        VAGroup = QtGui.QButtonGroup()
        HAGroup = QtGui.QButtonGroup()

        T_button = QtGui.QPushButton()
        M_button = QtGui.QPushButton()
        B_button = QtGui.QPushButton()

        VAGroup.addButton(T_button)
        VAGroup.addButton(M_button)
        VAGroup.addButton(B_button)

        L_button = QtGui.QPushButton()
        C_button = QtGui.QPushButton()
        R_button = QtGui.QPushButton()

        HAGroup.addButton(L_button)
        HAGroup.addButton(C_button)
        HAGroup.addButton(R_button)

        align_angle_row = QtGui.QHBoxLayout()
        align_angle_row.addWidget(VAGroup)
        align_angle_row.addWidget(HAGroup)

        wrap.insertLayout(align_angle_row, 1)







    def setTextObject(self, textObject):
        self.textObject = textObject
        self.setWindowTitle("Edit Style " + self.textObject.name)



    