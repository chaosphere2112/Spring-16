import pytest
import vcs
from PySide import QtCore, QtGui
import TextStyleEditor


@pytest.fixture
def editors():
    edit1 = TextStyleEditor.TextStyleEditorWidget()
    t = vcs.createtext()
    t.name = "header"
    edit1.setTextObject(t)

    edit2 = TextStyleEditor.TextStyleEditorWidget()
    t = vcs.createtext()
    t.name = "header"
    t.valign = 0
    t.halign = 1
    edit2.setTextObject(t)

    edit3 = TextStyleEditor.TextStyleEditorWidget()
    t = vcs.createtext()
    t.name = "header"
    t.valign = 4
    t.halign = 2
    edit3.setTextObject(t)

    return edit1, edit2, edit3


def save_check(name):
    assert name == "header"


def test_save(qtbot, editors):
    for editor in editors:

        editor.savePressed.connect(save_check)
        editor.save()


def test_alignment(editors):
    for editor in editors:
        # test valign
        editor.updateButton(editor.va_group.buttons()[0])
        assert editor.textObject.valign == 0

        editor.updateButton(editor.va_group.buttons()[2])
        assert editor.textObject.valign == 4

        editor.updateButton(editor.va_group.buttons()[1])
        assert editor.textObject.valign == 2

        # test halign
        editor.updateButton(editor.ha_group.buttons()[2])
        assert editor.textObject.halign == 2

        editor.updateButton(editor.ha_group.buttons()[1])
        assert editor.textObject.halign == 1

        editor.updateButton(editor.ha_group.buttons()[0])
        assert editor.textObject.halign == 0


def test_angle(editors):
    for editor in editors:

        assert editor.textObject.angle == 0

        editor.updateAngle(50)
        assert editor.textObject.angle == 50

        editor.updateAngle(440)
        assert editor.textObject.angle == 80


def test_font(editors):
    for editor in editors:
        editor.updateFont("Helvetica")
        assert editor.textObject.font == 4

        editor.updateFont("Chinese")
        assert editor.textObject.font == 8


def test_size(editors):
    for editor in editors:
        assert editor.textObject.height == 14

        editor.updateSize(50)
        assert editor.textObject.height == 50


def saveas_check(name):
    assert name == "test.txt"


def test_saveas(qtbot, editors):
    for editor in editors:

        editor.savePressed.connect(saveas_check)
        editor.saveAs()

        try:
            print editor.win
        except:
            print "Did not create save as dialog"
            assert 0

        editor.win.setTextValue("test.txt")
        qtbot.keyPress(editor.win, QtCore.Qt.Key_Enter)
