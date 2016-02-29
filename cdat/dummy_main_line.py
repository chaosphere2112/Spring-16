import vcs
from PySide import QtCore, QtGui
from cdat.LineEdit import LineEditor

def save(name):
    print name

if __name__ == "__main__":
    app = QtGui.QApplication([])

    line = vcs.createline("test")

    editor = LineEditor.LineEditorWidget()
    editor.savePressed.connect(save)

    editor.setLineObject(line)

    editor.show()
    editor.raise_()
    app.exec_()
