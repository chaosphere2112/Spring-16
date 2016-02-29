from cdat import vcswidget
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
