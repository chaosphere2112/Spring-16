from PySide import QtGui, QtCore
from cdat.Base import BaseWindow
from cdat.MarkEdit import MarkerPreview


class MarkerEditorWidget(BaseWindow.BaseWindowWidget):

    def __init__(self):
        super(MarkerEditorWidget, self).__init__()
        self.setPreview(MarkerPreview.MarkerPreviewWidget())

        # create labels
        type_label = QtGui.QLabel("Type:")
        color_label = QtGui.QLabel("Color:")
        size_label = QtGui.QLabel("Size:")

        row = QtGui.QHBoxLayout()

        # create type combo box
        type_box = QtGui.QComboBox()
        type_box.addItems(["dot", "plus", "star", "circle", "cross", "diamond", "triangle_up", "triangle_down", "triangle_left", "triangle_right", "square", "diamond_fill", "triangle_up_fill", "triangle_down_fill", "triangle_left_fill", "triangle_right_fill", "square_fill"])
        type_box.currentIndexChanged[str].connect(self.updateType)

        # create color spin box
        color_box = QtGui.QSpinBox()
        color_box.setRange(0, 255)
        color_box.valueChanged.connect(self.updateColor)

        # create size spin box
        size_box = QtGui.QSpinBox()
        size_box.setRange(1, 300)
        size_box.valueChanged.connect(self.updateSize)

        row.addWidget(type_label)
        row.addWidget(type_box)

        row.addWidget(color_label)
        row.addWidget(color_box)

        row.addWidget(size_label)
        row.addWidget(size_box)

        self.vertical_layout.insertLayout(1, row)

    def setMarkerObject(self, mark_obj):
        self.object = mark_obj
        self.preview.setMarkerObject(self.object)

    def updateType(self, cur_item):
        self.object.type = str(cur_item)
        self.preview.update()

    def updateColor(self, color):
        self.object.color = color
        self.preview.update()

    def updateSize(self, size):
        self.object.size = size
        self.preview.update()