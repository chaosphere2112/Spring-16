from PySide import QtGui, QtCore
import cdms2
import vcs
import SliderWidget


class LevelEditor(QtGui.QWidget):
    levelsChanged = QtCore.Signal(list)

    def __init__(self, variable, levels=None):
        super(LevelEditor, self).__init__()

        layout = QtGui.QVBoxLayout()
        self.set_title("%s Levels" % variable.id)
        self.variable = variable
        self._levels = levels

        self.level_label = QtGui.QLabel()

        def update_level_label(levels):
            self.level_label.setText(repr(levels))

        # Connect this to your object's signal
        def set_levels(levels):
            self.levels = levels

        minval, maxval = vcs.minmax(variable)
        if levels is None:
            levels = vcs.utils.mkscale(*vcs.minmax(self.variable))
        self.sliderWidget = SliderWidget.AdjustValues()
        self.sliderWidget.update(minval, maxval, levels)
        self.sliderWidget.valuesChanged.connect(set_levels)
        self.levelsChanged.connect(update_level_label)

        layout.addWidget(self.level_label)
        layout.addWidget(self.sliderWidget)
        self.setLayout(layout)

    def show(self):
        self.level_label.setText(repr(self.levels))
        super(LevelEditor, self).show()

    @property
    def levels(self):
        if self._levels is None:
            if self.variable is not None:
                return vcs.utils.mkscale(*vcs.minmax(self.variable))
            else:
                self._levels = []

        return self._levels

    @levels.setter
    def levels(self, levels):
        if levels is None:
            self._levels = None
            levels = self.levels

        if levels != self._levels:
            self._levels = levels
            self.levelsChanged.emit(levels)

    def set_title(self, title):
        # This will get swapped out with a label later
        self.setWindowTitle(title)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    cdmsfile = cdms2.open(vcs.sample_data + "/clt.nc")
    clt = cdmsfile("clt")
    le = LevelEditor(clt)
    le.show()
    le.raise_()
    le.activateWindow()
    app.exec_()
