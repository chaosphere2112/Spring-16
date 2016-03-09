import vtk
from PySide import QtCore, QtGui
import vcs
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from functools import partial


class QVCSWidget(QtGui.QFrame):
    """Simple embeddable QWidget that exposes a VCS canvas for use."""

    visibilityChanged = QtCore.Signal(bool)

    def __init__(self, parent=None):
        """Initialize the widget."""
        super(QVCSWidget, self).__init__(parent=parent)

        # Do the magic VTK embedding dance
        self.mRenWin = vtk.vtkRenderWindow()
        self.iren = QVTKRenderWindowInteractor(parent=self, rw=self.mRenWin)
        self.canvas = None

        self.canvasLayout = QtGui.QVBoxLayout()
        self.canvasLayout.addWidget(self.iren)
        self.setLayout(self.canvasLayout)

        self.becameVisible = partial(self.visibilityChanged.emit, True)
        self.becameHidden = partial(self.visibilityChanged.emit, False)

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                             QtGui.QSizePolicy.Expanding))

        self.visibilityChanged.connect(self.manageCanvas)
        self.displays = []
        self.to_plot = []

    def plot(self, *args, **kwargs):
        """
        Store all displays as items are plotted.

        Since the canvas is dismantled whenever this widget is hidden,
        we should recreate the plots that were being displayed whenever we
        show the widget again.
        """
        if self.canvas is not None:
            self.displays.append(self.canvas.plot(*args, **kwargs))
        else:
            self.to_plot.append((args, kwargs))

    def clear(self):
        """Reset the canvas and displays."""
        if self.canvas:
            self.canvas.clear()
        self.displays = []
        self.to_plot = []

    def update(self):
        if self.canvas:
            self.canvas.update()

    def manageCanvas(self, showing):
        """Make sure that the canvas isn't opened till we're really ready."""
        if showing and self.canvas is None:
            self.canvas = vcs.init(backend=self.mRenWin)
            self.canvas.open()
            for disp in self.displays:
                self.canvas.display_names.append(disp.name)
                if disp.name not in vcs.elements["display"]:
                    vcs.elements["display"][disp.name] = disp
            for args, kwargs in self.to_plot:
                self.displays.append(self.canvas.plot(*args, **kwargs))
            self.to_plot = []
            self.canvas.update()
        if not showing and self.canvas is not None:
            self.canvas.onClosing((0, 0))
            self.canvas = None

    def showEvent(self, e):
        "Handle twitchy VTK resources appropriately."
        super(QVCSWidget, self).showEvent(e)
        QtCore.QTimer.singleShot(0, self.becameVisible)

    def hideEvent(self, e):
        "Handle twitchy VTK resources appropriately."
        super(QVCSWidget, self).hideEvent(e)
        QtCore.QTimer.singleShot(0, self.becameHidden)

    def deleteLater(self):
        """
        Clean up the widget.

        Make sure to free render window resource when
        deallocating. Overriding PyQt deleteLater to free up
        resources
        """
        if self.canvas:
            self.canvas.onClosing((0, 0))
        self.canvas = None
        super(QVCSWidget, self).deleteLater()
