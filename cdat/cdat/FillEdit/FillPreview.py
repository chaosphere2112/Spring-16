from cdat import vcswidget
import vcs


class FillPreviewWidget(vcswidget.QVCSWidget):
    def __init__(self, parent=None):
        super(FillPreviewWidget, self).__init__(parent=parent)
        self.fillobj = None

    def setFillObject(self, fillobject):
        self.fillobj = fillobject
        tmpobj = vcs.createfillarea(source=self.fillobj)
        tmpobj.x = [.25, .25, .75, .75]
        tmpobj.y = [.25, .75, .75, .25]
        self.clear()
        self.plot(tmpobj)

    def update(self):
        self.setFillObject(self.fillobj)
