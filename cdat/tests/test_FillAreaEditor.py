import vcs, cdms2
from cdat.FillEdit import FillPreview


def test_preview():

    prev = FillPreview.FillPreviewWidget()
    fill = vcs.createfillarea()
    prev.setFillObject(fill)
    assert prev.fillobj == fill

    fill.style = "hatch"
    prev.update()

    assert prev.fillobj.style == ["hatch"]

