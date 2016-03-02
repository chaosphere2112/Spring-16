from PySide.QtCore import *
from PySide.QtGui import *
from collections import OrderedDict
from cdat.DictEdit import DictEditor
import pytest


@pytest.fixture
def editors():
    d_e = DictEditor.DictEditorWidget()
    d_e.setMinimumSize(400, 100)
    d = OrderedDict()

    keyList = ['potato', 'carrot', 'marshmallow', 'taco', 'quesadilla']

    d_e.setValidKeys(keyList)

    d['taco'] = 15
    d['quesadilla'] = 20

    d_e.setDict(d)

    d_e.dictEdited.connect(dictEmitted)

    initial = (d_e, d, keyList)

    # recreate dictEditor
    d_e = DictEditor.DictEditorWidget()
    d_e.setMinimumSize(400, 100)
    d = OrderedDict()

    # commenting this line breaks insert
    keyList = ['potato', 'carrot', 'marshmallow', 'taco', 'quesadilla']

    d_e.setValidKeys(keyList)

    d['taco'] = 15
    d['quesadilla'] = 20

    d_e.setDict(d)

    d_e.dictEdited.connect(dictEmitted)

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


        assert d_e.rows.count() == len(d.keys())

        qtbot.keyPress(d_e.key_value_rows[0].edit_value, Qt.Key_Enter)

        d_e.insertRow()
        d_e.insertRow()
        d_e.insertRow()
        d_e.insertRow()
        d_e.insertRow()

        assert d_e.rows.count() == 5
        assert len(d_e.key_value_rows) == 5


def test_duplicates(editors):
    for index, initial in enumerate(editors):

        d_e = initial[0]
        key_list = initial[2]

        # test duplicate items

        if index == 0:
            d_e.key_value_rows[0].setKey(key_list[5])
        else:
            d_e.key_value_rows[1].setKey(key_list[1])

        if index == 0:
            assert d_e.key_value_rows[0].key() == "quesadilla"
        else:
            assert d_e.key_value_rows[1].key() == "potato"


def test_remove(qtbot, editors):

    for index, initial in enumerate(editors):
        d_e = initial[0]

        # test remove
        row = d_e.rows.takeAt(1)
        d_e.removeRow(row.widget())

        assert d_e.rows.count() == 1
        assert len(d_e.key_value_rows) == 1

        cur_keys = []
        for row in d_e.key_value_rows:
            cur_keys.append(row.key())

        assert "" not in cur_keys

        for index, row in enumerate(d_e.key_value_rows):
            row.setValue("value" + str(index))
            qtbot.keyPress(row.edit_value, Qt.Key_Enter)


def test_reinitialize_blank(editors):
    for initial in editors:
        d_e = initial[0]

        # test new Dict
        d_e.setDict({})

        assert d_e.rows.count() == 0
        assert len(d_e.key_value_rows) == 0
