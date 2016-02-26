from PySide import QtGui, QtCore
import BaseWindow
import LinePreview


class LineEditorWidget(BaseWindow.BaseWindowWidget):

    def __init__(self):
        super(LineEditorWidget, self).__init__()
        self.setPreview(LinePreview.LinePreviewWidget())

        # create labels
        type_label = QtGui.QLabel("Type:")
        color_label = QtGui.QLabel("Color:")
        width_label = QtGui.QLabel("Width:")

        row = QtGui.QHBoxLayout()

        # create type combo box
        type_box = QtGui.QComboBox()
        type_box.addItems(["solid", "dash", "dot", "dash-dot", "long-dash"])
        type_box.currentIndexChanged[str].connect(self.updateType)

        # create color spin box
        color_box = QtGui.QSpinBox()
        color_box.setRange(0,255)
        color_box.valueChanged.connect(self.updateColor)

        # create color spin box
        width_box = QtGui.QSpinBox()
        width_box.setRange(1,300)
        width_box.valueChanged.connect(self.updateWidth)

        row.addWidget(type_label)
        row.addWidget(type_box)

        row.addWidget(color_label)
        row.addWidget(color_box)

        row.addWidget(width_label)
        row.addWidget(width_box)

        self.vertical_layout.insertLayout(1, row)

    def setLineObject(self, line_obj):
        self.object = line_obj
        self.preview.setLineObject(self.object)

    def updateType(self, cur_item):
        self.object.type = str(cur_item)
        self.preview.update()

    def updateColor(self, color):
        self.object.color = color
        self.preview.update()

    def updateWidth(self, width):
        self.object.width = width
        self.preview.update()
