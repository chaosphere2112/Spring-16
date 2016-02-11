from PySide.QtCore import *
from PySide.QtGui import *
from collections import OrderedDict
from KeyValueEditor import DictEditor
import pytest


@pytest.fixture
def editors():
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
    initial = (d_e, d, keyList)

    # recreate dictEditor
    d_e = DictEditor()
    d_e.setMinimumSize(400, 100)
    d = OrderedDict()

    # commenting this line breaks insert
    keyList = ['potato', 'carrot', 'marshmallow', 'taco', 'quesadilla']

    d_e.setValidKeys(keyList)

    d['taco'] = 15
    d['quesadilla'] = 20

    d_e.setDict(d)

    d_e.dictEdited.connect(dictEmitted)

    d_e.show()
    d_e.raise_()
    new_d = OrderedDict()
    new_d['potato'] = 1
    new_d['carrot'] = 2
    d_e.setDict(new_d)
    reinitial = (d_e, d, keyList)
    return (initial, reinitial)



def dictEmitted(d):

    print "D:", d
    for key, value in d.items():
        print str(key) + ": " + str(value)
        assert key != "" and value != ""


def test_insert(qtbot, editors):

    for initial in editors:
        d_e = initial[0]
        d = initial[1]
        keyList = initial[2]


        assert d_e.row_count == len(d.keys())

        qtbot.keyPress(d_e.valueEdits[0], Qt.Key_Enter)

        d_e.insertRow()
        d_e.insertRow()
        d_e.insertRow()
        d_e.insertRow()
        d_e.insertRow()

        assert d_e.row_count == 5
        assert len(d_e.cBoxes) == 5

        # populate empty combo boxes
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


def test_duplicates(editors):
    for index, initial in enumerate(editors):

        d_e = initial[0]

        # test duplicate items

        if index == 0:
            d_e.cBoxes[0].setCurrentIndex(5)
        else:
            d_e.cBoxes[1].setCurrentIndex(1)

        print d_e.keys

        if index == 0:
            assert d_e.cBoxes[0].itemText(d_e.cBoxes[0].currentIndex()) == "quesadilla"
            assert d_e.cBoxes[1].itemText(d_e.cBoxes[1].currentIndex()) == "" and d_e.cBoxes[1].currentIndex() == 0
        else:
            assert d_e.cBoxes[1].itemText(d_e.cBoxes[1].currentIndex()) == "potato"
            assert d_e.cBoxes[0].itemText(d_e.cBoxes[0].currentIndex()) == "" and d_e.cBoxes[0].currentIndex() == 0


def test_remove(qtbot, editors):

    for index, initial in enumerate(editors):
        d_e = initial[0]

        # test remove
        d_e.removeRow(d_e.rows.itemAt(1), 1)

        assert d_e.row_count == 1
        assert len(d_e.cBoxes) == 1

        # d_e.cBoxes[1].setCurrentIndex(2)
        assert "" not in d_e.keys

        for index, value in enumerate(d_e.valueEdits):
            value.setText("value" + str(index))
            qtbot.keyPress(value, Qt.Key_Enter)


def test_reinitialize_blank(editors):
    for initial in editors:
        d_e = initial[0]

        # test new Dict
        d_e.setDict({})

        assert d_e.row_count == 0
        assert len(d_e.cBoxes) == 0
