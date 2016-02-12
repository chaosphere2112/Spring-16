import vcswidget
import vcs


class TextStylePreviewWidget(vcswidget.QVCSWidget):
    def __init__(self, parent=None):
        super(TextStylePreviewWidget, self).__init__(parent=parent)
        self.textobj = None

    def setTextObject(self, textobject):
        self.textobj = textobject
        tmpobj = vcs.createtext(Tt_source=self.textobj.Tt, To_source=self.textobj.To)
        tmpobj.string = ["%s Preview" % self.textobj.name]
        tmpobj.x = [.5]
        tmpobj.y = [.5]
        self.clear()
        self.plot(tmpobj)

    def update(self):
        self.setTextObject(self.textobj)


if __name__ == "__main__":
    from PySide import QtGui
    app = QtGui.QApplication([])
    widget = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    widget.setLayout(layout)
    preview = TextStylePreviewWidget()
    layout.addWidget(preview)

    line_edit = QtGui.QLineEdit()
    
    def make_tc(name):
        tc = vcs.createtext(name)
        preview.setTextObject(tc)

    line_edit.textEdited.connect(make_tc)
    layout.addWidget(line_edit)
    widget.show()
    widget.raise_()
    app.exec_()