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


    d['taco'] = 15
    d['quesadilla'] = 20

    d_e.setDict(d)

    d_e.dictEdited.connect(dictEmitted)

    initial = (d_e, d)

    # recreate dictEditor
    d_e = DictEditor()
    d_e.setMinimumSize(400, 100)
    d = OrderedDict()

    d['taco'] = 15
    d['quesadilla'] = 20

    d_e.setDict(d)

    d_e.dictEdited.connect(dictEmitted)

    new_d = OrderedDict()
    new_d['potato'] = 1
    new_d['carrot'] = 2
    d_e.setDict(new_d)
    reinitial = (d_e, new_d)
    print "Finished initialize for both"
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

        # checking initial values
        for i in d_e.textEdits:
            assert i.text() != ""
            assert i.text() in d.keys()

        # check insert row
        d_e.insertRow()
        d_e.insertRow()
        d_e.insertRow()
        d_e.insertRow()

        for index, edit in enumerate(d_e.textEdits):
            if edit.text() == "":

                # test blank key edge case
                qtbot.keyPress(d_e.textEdits[index], Qt.Key_Enter)

                # edit key
                edit.setText("test" + str(index))

                # test blank value edge case
                qtbot.keyPress(d_e.textEdits[index], Qt.Key_Enter)

                # edit value
                d_e.valueEdits[index].setText("value" + str(index))
                qtbot.keyPress(d_e.valueEdits[index], Qt.Key_Enter)
        assert d_e.row_count == 6
        assert len(d_e.textEdits) == 6


def test_remove(editors):

    for initial in editors:
        d_e = initial[0]

        # check delete
        d_e.removeRow(d_e.rows.itemAt(1), 1)

        assert d_e.row_count == 1
        assert len(d_e.textEdits) == 1


def test_color_change(qtbot, editors):

    for index, initial in enumerate(editors):

        d_e = initial[0]

        d_e.textEdits[1].setText("pizza")
        qtbot.keyPress(d_e.textEdits[1], Qt.Key_Enter)

        if index == 0:
            correct_keys = ['taco', 'pizza']
        else:
            correct_keys = ['potato', 'pizza']

        cur_keys = []
        for i in d_e.textEdits:
            cur_keys.append(i.text())

        print cur_keys
        print correct_keys
        assert cur_keys == correct_keys
        assert correct_keys == d_e.keys

        qtbot.keyPress(d_e.textEdits[1], Qt.Key_Enter)

        # check invalid input
        d_e.textEdits[0].setText('pizza')

        color = d_e.textEdits[0].styleSheet()
        assert color == "color: rgb(255, 0, 0);"

        color = d_e.textEdits[1].styleSheet()
        assert color == "color: rgb(0, 0, 0);"

        d_e.textEdits[0].setText('pineapple')
        color = d_e.textEdits[0].styleSheet()
        assert color == "color: rgb(0, 0, 0);"

        qtbot.keyPress(d_e.textEdits[1], Qt.Key_Enter)

        cur_keys = []
        for i in d_e.textEdits:
            cur_keys.append(i.text())
        print cur_keys

        assert d_e.validKeys() == None

def test_return_dict(editors):

    for initial in editors:

        d_e = initial[0]
        d = initial[1]

        return_d = d_e.dict()

        for key in d.keys():
            assert return_d[key] == d[key]
            assert key in return_d.keys()

