import vcs
from PySide import QtCore, QtGui
from cdat.FillEdit import FillAreaEditor

def save(name):
    print name

if __name__ == "__main__":
    app = QtGui.QApplication([])

    fill = vcs.createfillarea("test")

    editor = FillAreaEditor.FillAreaEditorWidget()
    editor.savePressed.connect(save)
    editor.setFillObject(fill)

    editor.show()
    editor.raise_()
    app.exec_()