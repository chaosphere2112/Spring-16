from PySide import QtGui, QtCore
from cdat.Base import BaseSaveWindow
from cdat.MarkEdit import MarkerPreview


class MarkerEditorWidget(BaseSaveWindow.BaseSaveWindowWidget):

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
        type_box.addItems(["dot", "plus", "star", "circle", "cross", "diamond", "triangle_up", "triangle_down",
                           "triangle_left", "triangle_right", "square", "diamond_fill", "triangle_up_fill",
                           "triangle_down_fill", "triangle_left_fill", "triangle_right_fill", "square_fill",'hurricane',
                           'w00', 'w01', 'w02', 'w03', 'w04', 'w05', 'w06', 'w07', 'w08', 'w09', 'w10', 'w11', 'w12',
                           'w13', 'w14', 'w15', 'w16', 'w17', 'w18', 'w19', 'w20', 'w21', 'w22', 'w23', 'w24', 'w25',
                           'w26', 'w27', 'w28', 'w29', 'w30', 'w31', 'w32', 'w33', 'w34', 'w35', 'w36', 'w37', 'w38',
                           'w39', 'w40', 'w41', 'w42', 'w43', 'w44', 'w45', 'w46', 'w47', 'w48', 'w49', 'w50', 'w51',
                           'w52', 'w53', 'w54', 'w55', 'w56', 'w57', 'w58', 'w59', 'w60', 'w61', 'w62', 'w63', 'w64',
                           'w65', 'w66', 'w67', 'w68', 'w69', 'w70', 'w71', 'w72', 'w73', 'w74', 'w75', 'w76', 'w77',
                           'w78', 'w79', 'w80', 'w81', 'w82', 'w83', 'w84', 'w85', 'w86', 'w87', 'w88', 'w89', 'w90',
                           'w91', 'w92', 'w93', 'w94', 'w95', 'w96', 'w97', 'w98', 'w99', 'w100', 'w101', 'w102'])
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