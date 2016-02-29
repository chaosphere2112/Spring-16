import pytest
import vcs, cdms2
from PySide import QtGui, QtCore
from cdat.LineEdit import LineEditor

@pytest.fixture
def editor():
    editor = LineEditor.LineEditorWidget()
    line = vcs.createline()
    editor.setLineObject(line)
    return editor

def test_type(qtbot, editor):
    editor.updateType('dash')
    assert editor.object.type == ['dash']

def test_color(qtbot, editor):
    editor.updateColor(55)
    assert editor.object.color == [55]

def test_width(qtbot, editor):
    editor.updateWidth(250)
    assert editor.object.width == [250]

