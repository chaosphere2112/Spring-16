from PySide.QtCore import *
from PySide.QtGui import *
from collections import OrderedDict
from dict import DictEditor

d_e = None

def dictEmitted(dict):


    print "D:", dict
    for key, value in dict.items():
        print str(key) + ": " + str(value)
        assert key in d_e.keys
        assert value in d_e.values
        assert d_e.keys.index(key) == d_e.values.index(value)


def test_initialize(qtbot):
    global d_e
    d_e = DictEditor()
    d_e.setMinimumSize(400, 100)
    d = OrderedDict()

    keyList = ['potato', 'carrot', 'marshmallow', 'taco', 'quesadilla']

    d_e.setValidKeys(keyList)

    d['taco'] = 15
    d['quesadilla'] = 20

    d_e.setDict(d)


    d_e.dictEdited.connect(dictEmitted)

    d_e.show()
    d_e.raise_()

    assert d_e.row_count == len(d.keys())

    qtbot.keyPress(d_e.valueEdits[0], Qt.Key_Enter)

    qtbot.mouseClick(d_e.add_button, Qt.LeftButton)
    qtbot.mouseClick(d_e.add_button, Qt.LeftButton)

    assert len(d_e.cBoxes) == 4

    texts = []
    c = 0
    for i in d_e.cBoxes:
        t = i.itemText(i.currentIndex())
        if t not in texts:
            texts.append(t)

        if t == "":
            while keyList[c] in texts:
                c += 1
            index = i.findText(keyList[c])
            i.setCurrentIndex(index)
            texts.append(i.itemText(i.currentIndex()))

    for i in d_e.cBoxes:
        print d_e.cBoxes.index(i)
        assert i.itemText(i.currentIndex()) != ""

    qtbot.mouseClick









