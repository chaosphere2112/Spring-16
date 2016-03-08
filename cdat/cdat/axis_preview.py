import vcs
from cdat import vcswidget


class AxisPreviewWidget(vcswidget.QVCSWidget):
    def __init__(self, parent=None):
        super(AxisPreviewWidget, self).__init__(parent=parent)
        self.axis = None
        self.visibilityChanged.connect(self.visibility_toggled)

    def visibility_toggled(self, showing):
        if showing:
            self.update()

    def update(self):

        if self.canvas is None:
            return
        self.canvas.clear(render=False)
        template = vcs.createtemplate(source=self.axis.tmpl)
        template.blank()

        axis_orientation = self.axis._axis[0]
        axis_number = self.axis._axis[1]
        axis_ticks = getattr(template, "%stic%s" % (axis_orientation, axis_number))
        axis_min_ticks = getattr(template, "%smintic%s" % (axis_orientation, axis_number))
        axis_labels = getattr(template, "%slabel%s" % (axis_orientation, axis_number))

        # Make the ticks visible
        axis_ticks.priority = 1
        axis_min_ticks.priority = 1 if self.axis.show_miniticks else 0
        axis_labels.priority = 1

        moving_attr = "x" if axis_orientation == "y" else "y"
        attr_1 = moving_attr + "1"
        attr_2 = moving_attr + "2"

        ticklen = getattr(axis_ticks, attr_2) - getattr(axis_ticks, attr_1)
        label_distance = getattr(axis_labels, moving_attr) - getattr(axis_ticks, attr_1)
        minticklen = getattr(axis_min_ticks, attr_2) - getattr(axis_min_ticks, attr_1)

        # Move the ticks to the middle
        setattr(axis_ticks, attr_1, .5)
        setattr(axis_ticks, attr_2, .5 + ticklen)
        setattr(axis_min_ticks, attr_1, .5)
        setattr(axis_min_ticks, attr_2, .5 + minticklen)
        setattr(axis_labels, moving_attr, .5 + label_distance)

        # Get the worldcoordinates
        try:
            wc = vcs.utils.getworldcoordinates(self.axis.gm, self.axis.var.getAxis(-1), self.axis.var.getAxis(-2))
        except:
            # 1D
            wc = vcs.utils.getworldcoordinates(self.axis.gm, range(len(self.axis.var)), self.axis.var)
        template.drawTicks(self.axis.var, self.axis.gm, self.canvas, axis_orientation, axis_number,
                           (template.data.x1, template.data.x2, template.data.y1, template.data.y2), wc)
        self.canvas.backend.renWin.Render()

    def resizeEvent(self, ev):
        super(AxisPreviewWidget, self).resizeEvent(ev)
        self.update()

    def setAxisObject(self, axis):
        self.axis = axis