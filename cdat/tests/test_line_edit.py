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

    d['taco'] = 15
    d['quesadilla'] = 20

    d_e.setDict(d)

    d_e.dictEdited.connect(dictEmitted)

    initial = (d_e, d)

    # recreate dictEditor
    d_e = DictEditor.DictEditorWidget()
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
        for row in d_e.key_value_rows:
            assert row.key != ""
            assert row.key() in d.keys()
            assert row.value != ""

        # check insert row
        d_e.insertRow()
        d_e.insertRow()
        d_e.insertRow()
        d_e.insertRow()

        for index, row in enumerate(d_e.key_value_rows):

            if row.key() == "":
                # test blank key edge case
                qtbot.keyPress(row.edit_key, Qt.Key_Enter)

                # edit key
                row.setKey("test" + str(index))

                # test blank value edge case
                qtbot.keyPress(row.edit_key, Qt.Key_Enter)

                # edit value
                row.setValue("value" + str(index))
                qtbot.keyPress(row.edit_key, Qt.Key_Enter)

        assert d_e.rows.count() == 6
        assert len(d_e.key_value_rows) == 6


def test_remove(editors):
    for initial in editors:
        d_e = initial[0]

        # check delete
        row = d_e.rows.takeAt(0)
        d_e.removeRow(row.widget())

        assert d_e.rows.count() == 1
        assert len(d_e.key_value_rows) == 1


def test_color_change(qtbot, editors):
    for index, initial in enumerate(editors):

        d_e = initial[0]

        d_e.key_value_rows[1].setKey("pizza")
        qtbot.keyPress(d_e.key_value_rows[1].edit_key, Qt.Key_Enter)

        if index == 0:
            correct_keys = ['taco', 'pizza']
        else:
            correct_keys = ['potato', 'pizza']

        cur_keys = []
        for row in d_e.key_value_rows:
            cur_keys.append(row.key())

        print cur_keys

        print correct_keys
        assert cur_keys == correct_keys

        qtbot.keyPress(d_e.key_value_rows[1].edit_key, Qt.Key_Enter)

        # check invalid input
        d_e.key_value_rows[0].setKey('pizza')
        qtbot.keyPress(d_e.key_value_rows[0].edit_key, Qt.Key_Enter)

        cur_keys = []
        for row in d_e.key_value_rows:
            cur_keys.append(row.key())

        print cur_keys


        color = d_e.key_value_rows[0].edit_key.styleSheet()
        assert color == "color: rgb(255, 0, 0);"

        color = d_e.key_value_rows[1].edit_key.styleSheet()
        assert color == "color: rgb(0, 0, 0);"

        d_e.key_value_rows[0].setKey('pineapple')
        qtbot.keyPress(d_e.key_value_rows[0].edit_key, Qt.Key_Enter)

        color = d_e.key_value_rows[0].edit_key.styleSheet()
        assert color == "color: rgb(0, 0, 0);"

        qtbot.keyPress(d_e.key_value_rows[1].edit_key, Qt.Key_Enter)

        cur_keys = []
        for row in d_e.key_value_rows:
            cur_keys.append(row.key())
        print cur_keys

        assert d_e.validKeys() == None


def test_return_dict(editors):
    for initial in editors:

        d_e = initial[0]
        d = initial[1]

        return_d = d_e.dict()

        for key in d.keys():
            assert return_d[key] == str(d[key])
            assert key in return_d.keys()
