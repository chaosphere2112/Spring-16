from PySide import QtCore, QtGui
import cdms2
import vcs
from SliderWidget import AdjustValues
import pytest


@pytest.fixture
def adjuster():
    print "start setup"
    cdmsfile = cdms2.open(vcs.sample_data + "/clt.nc")
    clt = cdmsfile("clt")
    min, max = vcs.minmax(clt)
    levels = vcs.utils.mkscale(*vcs.minmax(clt))

    edit = AdjustValues()
    edit.update(min, max, levels)

    print "finished setup"
    return edit, levels


def test_insert(qtbot, adjuster):
    adj = adjuster[0]
    levels = adjuster[1]

    assert len(adj.slides) == 11

    for index, slide in enumerate(adj.slides):
        assert levels[index] == slide.sliderPosition()

    adj.add_level()
    adj.add_level()

    assert len(adj.slides) == 13


def test_move(adjuster):
    adj = adjuster[0]

    assert len(adj.slides) == 11

    adj.slides[4].setValue(8)

    for i in range(1, 5):
        assert adj.slides[i].sliderPosition() == 8

    adj.slides[5].setValue(92)

    for i in range(5, 10):
        assert adj.slides[i].sliderPosition() == 92


def test_reupdate(adjuster):
    adj = adjuster[0]

    new_vals = [1, 2, 5, 8, 20, 45, 70, 155, 139]
    adj.update(0, 200, new_vals)

    correct_vals = [1, 2, 5, 8, 20, 45, 70, 139, 139]
    cur_vals = []

    for i in adj.slides:
        cur_vals.append(i.sliderPosition())

    assert cur_vals == correct_vals


def test_bad_minmax(adjuster):
    adj = adjuster[0]

    new_vals = [1, 2, 5, 8, 20, 45, 70, 139, 150]

    with pytest.raises(ValueError):
        adj.update(100, 0, new_vals)


def test_remove(adjuster):

    adj = adjuster[0]
    levels = adjuster[1]

    levels.remove(levels[3])
    adj.remove_level(adj.rows[3])

    cur_vals = []
    for i in adj.slides:
        cur_vals.append(i.sliderPosition())

    assert cur_vals == levels





