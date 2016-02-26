from __future__ import print_function
import vcs, cdms2
from PySide import QtGui, QtCore
import LineEditor

app = QtGui.QApplication([])

editor = LineEditor.LineEditorWidget()
editor.setMinimumSize(400,400)

line = vcs.createline("test_line")

line.list()

editor.setLineObject(line)
editor.savePressed.connect(lambda name: print (name))

editor.show()
editor.raise_()



app.exec_()
