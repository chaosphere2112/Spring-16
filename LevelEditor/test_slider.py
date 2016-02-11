from PySide import QtCore, QtGui
import cdms2
import vcs
import SliderWidget
import pytest


@pytest.fixture
def adjuster():
    cdmsfile = cdms2.open(vcs.sample_data + "/clt.nc")
    clt = cdmsfile("clt")
    min, max = vcs.minmax(clt)
    levels = vcs.utils.mkscale(*vcs.minmax(clt))
    print len(levels)

    edit = SliderWidget.AdjustValues()
    edit.update(min, max, levels)
    first = (edit, levels, min, max)

    edit = SliderWidget.AdjustValues()
    edit.update(min, max, levels)

    new_vals = [1, 2, 5, 8, 20, 45, 70, 155, 139]
    min = 0
    max = 200
    edit.update(min, max, new_vals)

    second = (edit, new_vals, min, max)

    return first, second


def test_insert(qtbot, adjuster):
    for index, state in enumerate(adjuster):

        adj = state[0]
        levels = state[1]
        max = state[3]
        if index == 0:
            assert len(adj.slides) == 11
        else:
            assert len(adj.slides) == 9
            levels[7] = 139


        for i, slide in enumerate(adj.slides):
            print i
            assert levels[i] == slide.sliderPosition()

        levels.append(max)
        levels.append(max)
        adj.add_level()
        adj.add_level()

        if index == 0:
            assert len(adj.slides) == 13
        else:
            assert len(adj.slides) == 11

        cur_vals = []
        for i in adj.slides:
            cur_vals.append(i.sliderPosition())

        assert cur_vals == levels

        # remove
        del levels[7]
        adj.remove_level(adj.rows[7])

        if index == 0:
            assert len(adj.slides) == 12
        else:
            assert len(adj.slides) == 10

        cur_vals = []
        for i in adj.slides:
            cur_vals.append(i.sliderPosition())

        assert cur_vals == levels

        # insert
        adj.add_level()

        if index == 0:
            assert len(adj.slides) == 13
            assert adj.slides[-1].sliderPosition() == 100
        else:
            assert len(adj.slides) == 11
            assert adj.slides[-1].sliderPosition() == 200


def test_move(adjuster):

    for index, state in enumerate(adjuster):

        adj = state[0]
        print "INDEX:", index
        if index == 0:
            adj.slides[4].setValue(8)

            for i in range(1, 5):
                assert adj.slides[i].sliderPosition() == 8

            adj.slides[5].setValue(92)

            for i in range(5, 10):
                assert adj.slides[i].sliderPosition() == 92

        else:

            adj.slides[4].setValue(1)
            for i in range(1, 5):
                assert adj.slides[i].sliderPosition() == 1

            adj.slides[5].setValue(180)

            for i in range(5, len(adj.slides)):
                assert adj.slides[i].sliderPosition() == 180




        # test after insert

        adj.add_level()
        adj.add_level()


        adj.slides[-1].setValue(65)

        for i in range(6, len(adj.slides)):
            assert adj.slides[i].sliderPosition() == 65

        # after remove twice

        adj.remove_level(adj.rows[4])
        adj.remove_level(adj.rows[4])

        cur_vals = []
        for i in adj.slides:
            cur_vals.append(i.sliderPosition())
        print cur_vals


        if index == 0:
            adj.slides[2].setValue(60)

            for i in range(2, 4):
                assert adj.slides[i].sliderPosition() == 60

            adj.slides[9].setValue(35)

            for i in range(2, 9):
                assert adj.slides[i].sliderPosition() == 35

        else:

            adj.slides[2].setValue(113)
            for i in range(2, 4):
                assert adj.slides[i].sliderPosition() == 113

            adj.slides[7].setValue(44)


            cur_vals = []
            for i in adj.slides:
                cur_vals.append(i.sliderPosition())
            print cur_vals


            for i in range(2, len(adj.slides)-1):
                assert adj.slides[i].sliderPosition() == 44


def test_reupdate(adjuster):
    # check if update worked correctly
    adj = adjuster[1][0]

    correct_vals = [1, 2, 5, 8, 20, 45, 70, 139, 139]
    cur_vals = []

    for i in adj.slides:
        cur_vals.append(i.sliderPosition())

    assert cur_vals == correct_vals


def test_bad_minmax(adjuster):
    # check if error raised on bad update
    for state in adjuster:
        adj = state[0]

        new_vals = [1, 2, 5, 8, 20, 45, 70, 139, 150]

        with pytest.raises(ValueError):
            adj.update(100, 0, new_vals)


def test_remove(adjuster):

    for index, state in enumerate(adjuster):
        adj = state[0]
        levels = state[1]

        if index == 1:
            levels[7] = 139

        del levels[3]
        adj.remove_level(adj.rows[3])

        cur_vals = []
        for i in adj.slides:
            cur_vals.append(i.sliderPosition())

        assert cur_vals == levels





