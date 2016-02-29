import pytest
import vcs, cdms2
from PySide import QtGui, QtCore
from cdat.LineEdit import LinePreview


def test_preview():
    prev = LinePreview.LinePreviewWidget()
    line = vcs.createline()
    prev.setLineObject(line)
    assert prev.lineobj == line

    line.type = "dot"
    prev.update()

    assert prev.lineobj.type == ["dot"]