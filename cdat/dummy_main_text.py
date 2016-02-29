import vcs
from PySide import QtCore, QtGui
from cdat.TextEdit import TextStyleEditor

if __name__ == "__main__":
    print "start"
    app = QtGui.QApplication([])

    text = vcs.createtext()
    text.name = "test"

    editor = TextStyleEditor.TextStyleEditorWidget()

    editor.setTextObject(text)

    editor.show()
    editor.raise_()
    app.exec_()
