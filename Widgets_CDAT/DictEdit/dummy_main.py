from PySide.QtCore import *
from PySide.QtGui import *
from KeyValueEditor import DictEditor
from collections import OrderedDict

def dictEmitted(dict):
    print "D:", dict
    for key, value in dict.items():
        print str(key) + ": " + str(value)


if __name__ == "__main__":

    app = QApplication([])

    d_e = DictEditor()
    d_e.setMinimumSize(400, 100)
    d = OrderedDict()

    # d_e.setValidKeys(['potato', 'carrot', 'marshmallow', 'taco', 'quesadilla'])

    d['taco'] = 15
    d['quesadilla'] = 20

    d_e.setDict(d)


    d_e.dictEdited.connect(dictEmitted)

    d_e.show()
    d_e.raise_()

    # d = OrderedDict()
    # d['cheese'] = 20

    # d_e.setDict(d)

    app.exec_()
