import vcs, cdms2
from cdat.MarkEdit import MarkerPreview


def test_preview():
    prev = MarkerPreview.MarkerPreviewWidget()
    marker = vcs.createmarker("test")
    prev.setMarkerObject(marker)
    assert prev.markerobj == marker

    marker.type = "cross"
    prev.update()

    assert prev.markerobj.type == ["cross"]