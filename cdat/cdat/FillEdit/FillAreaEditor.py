import cdms2, vcs
from PySide import QtGui, QtCore
from cdat.Base import BaseSaveWindow
from cdat.FillEdit import FillPreview


class FillAreaEditorWidget(BaseSaveWindow.BaseSaveWindowWidget):

    def __init__(self):
        super(FillAreaEditorWidget, self).__init__()
        self.setPreview(FillPreview.FillPreviewWidget())

        # Create Labels
        style_label = QtGui.QLabel("Style: ")
        index_label = QtGui.QLabel("Index: ")
        color_label = QtGui.QLabel("Color: ")
        opacity_label = QtGui.QLabel("Opacity: ")

        # create style combo box
        style_box = QtGui.QComboBox()
        style_box.addItems(["solid", "hatch", "pattern"])
        style_box.currentIndexChanged[str].connect(self.updateStyle)

        # create color spin box
        color_box = QtGui.QSpinBox()
        color_box.setRange(0, 255)
        color_box.valueChanged.connect(self.updateColor)

        # create color spin box
        index_box = QtGui.QSpinBox()
        index_box.setRange(1, 20)
        index_box.valueChanged.connect(self.updateIndex)

        opacity_slider = QtGui.QSlider()
        opacity_slider.setRange(1, 100)
        opacity_slider.setOrientation(QtCore.Qt.Horizontal)
        opacity_slider.setValue(100)
        opacity_slider.setTickPosition(QtGui.QSlider.TicksAbove)
        opacity_slider.valueChanged.connect(self.updateOpacity)

        style_color_row = QtGui.QHBoxLayout()
        index_opacity_row = QtGui.QHBoxLayout()

        style_color_row.addWidget(style_label)
        style_color_row.addWidget(style_box)

        style_color_row.addWidget(color_label)
        style_color_row.addWidget(color_box)

        index_opacity_row.addWidget(index_label)
        index_opacity_row.addWidget(index_box)

        index_opacity_row.addWidget(opacity_label)
        index_opacity_row.addWidget(opacity_slider)

        self.vertical_layout.insertLayout(1, style_color_row)
        self.vertical_layout.insertLayout(2, index_opacity_row)

    def setFillObject(self, fill_object):
        self.object = fill_object
        self.preview.setFillObject(self.object)


    def updateStyle(self, cur_item):
        self.object.style = str(cur_item)
        self.preview.update()

    def updateColor(self, color):
        self.object.color = color
        self.preview.update()

    def updateIndex(self, index):
        self.object.index = index
        self.preview.update()

    def updateOpacity(self, level):
        self.object.opacity = level
        self.preview.update()
