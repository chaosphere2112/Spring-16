import pytest
import vcs, cdms2
from cdat.FillEdit import FillAreaEditor

@pytest.fixture
def editor():
    editor = FillAreaEditor.FillAreaEditorWidget()
    fill = vcs.createfillarea()
    editor.setFillObject(fill)
    return editor

def test_style(qtbot, editor):
    editor.updateStyle('hatch')
    assert editor.object.style == ['hatch']

def test_color(qtbot, editor):
    editor.updateColor(55)
    assert editor.object.color == [55]

def test_index(qtbot, editor):
    editor.updateIndex(13)
    assert editor.object.index == [13]

def test_opacity(qtbot, editor):
    editor.updateOpacity(40)
    assert editor.object.opacity == [40]
