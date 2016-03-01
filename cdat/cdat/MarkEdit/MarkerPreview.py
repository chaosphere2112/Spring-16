from cdat import vcswidget
import vcs


class MarkerPreviewWidget(vcswidget.QVCSWidget):
    def __init__(self, parent=None):
        super(MarkerPreviewWidget, self).__init__(parent=parent)
        self.markerobj = None

    def setMarkerObject(self, markerobject):
        self.markerobj = markerobject
        tmpobj = vcs.createmarker(source=self.markerobj)
        tmpobj.x = [.5, .5]
        tmpobj.y = [.5, .5]
        self.clear()
        self.plot(tmpobj)

    def update(self):
        self.setMarkerObject(self.markerobj)
