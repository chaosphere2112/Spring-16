from cdat import vcswidget
import vcs


class LinePreviewWidget(vcswidget.QVCSWidget):
    def __init__(self, parent=None):
        super(LinePreviewWidget, self).__init__(parent=parent)
        self.lineobj = None

    def setLineObject(self, lineobject):
        self.lineobj = lineobject
        tmpobj = vcs.createline(source=self.lineobj)
        tmpobj.x = [.25, .75]
        tmpobj.y = [.5, .5]
        self.clear()
        self.plot(tmpobj)

    def update(self):
        self.setLineObject(self.lineobj)
