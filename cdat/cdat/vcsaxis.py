import vcs

class VCSAxis(object):
    def __init__(self, gm, tmpl, axis, var):
        self.gm = gm
        self.tmpl = tmpl
        self._axis = axis
        self.var = var

    @property
    def axis(self):
        if self._axis[0] == "x":
            try:
                return self.var.getAxis(-1)
            except:
                return range(len(self.var))
        elif self._axis[0] == "y":
            try:
                return self.var.getAxis(-2)
            except:
                return self.var
        return None

    @property
    def ticks(self):
        """Use this attribute for the dict editor."""
        val = None
        if self._axis == "x1":
            val = self.gm.xticlabels1
        elif self._axis == "x2":
            val = self.gm.xticlabels2
        elif self._axis == "y1":
            val = self.gm.yticlabels1
        elif self._axis == "y2":
            val = self.gm.yticlabels2
        return val

    @ticks.setter
    def ticks(self, val):
        """Use this attribute for the dict editor."""
        if self.show_miniticks:
            minitick_count = self.minitick_count
        else:
            minitick_count = 0
        if self._axis == "x1":
            self.gm.xticlabels1 = val
        if self._axis == "x2":
            self.gm.xticlabels2 = val
        if self._axis == "y1":
            self.gm.yticlabels1 = val
        if self._axis == "y2":
            self.gm.yticlabels2 = val
        if minitick_count != 0:
            self.minitick_count = minitick_count
        if isinstance(val, str):
            # Check if there exists a listname_miniticks and assign that to miniticks
            if "%s_miniticks" % val in vcs.elements["list"]:
                self.miniticks = vcs.elements['list']["%s_miniticks" % val]

    @property
    def miniticks(self):
        """Used internally."""
        if self._axis == "x1":
            return self.gm.xmtics1
        elif self._axis == "x2":
            return self.gm.xmtics2
        elif self._axis == "y1":
            return self.gm.ymtics1
        elif self._axis == "y2":
            return self.gm.ymtics2

    @miniticks.setter
    def miniticks(self, val):
        """Used internally."""
        if self._axis == "x1":
            self.gm.xmtics1 = val
        if self._axis == "x2":
            self.gm.xmtics2 = val
        if self._axis == "y1":
            self.gm.ymtics1 = val
        if self._axis == "y2":
            self.gm.ymtics2 = val

    @property
    def mode(self):
        if self.ticks == "*" or str(self.ticks) in vcs.elements["list"]:
            return "auto"
        if self.step is not None:
            return "even"
        else:
            return "manual"

    @mode.setter
    def mode(self, value):
        if value == "auto" and isinstance(self.ticks, dict):
            self.ticks = "*"

    @property
    def numticks(self):
        if isinstance(self.ticks, dict):
            return len(self.ticks)
        return None

    @numticks.setter
    def numticks(self, num):
        if num > 0:
            # Interpolate between left and right num times
            left, right = vcs.minmax(self.axis)
            step = (right - left) / float(num)
            self.ticks = {left + n * step: left + n * step for n in range(num)}
        else:
            left, right = vcs.minmax(self.axis)
            step = (right - left) / float(num)
            self.ticks = {right + n * step: right + n * step for n in range(-1 * num)}

    @property
    def step(self):
        ticks = self.ticks
        if isinstance(ticks, str):
            ticks = vcs.elements["list"][ticks]
        ticks = sorted(ticks)
        left, right = vcs.minmax(self.axis)
        return (right - left) / len(ticks)

    @step.setter
    def step(self, value):
        left, right = vcs.minmax(self.axis)
        tick_vals = []

        value = float(value)
        if value < 0:
            cur_val = right
            target = left
            comp = target.__lt__
        else:
            cur_val = left
            target = right
            comp = target.__gt__

        while comp(cur_val):
            tick_vals.append(cur_val)
            cur_val += value

        self.ticks = {i: i for i in tick_vals}

    @property
    def show_miniticks(self):
        """Use this attribute for the dict editor."""
        if self._axis == "x1":
            return self.tmpl.xmintic1.priority > 0
        elif self._axis == "x2":
            return self.tmpl.xmintic2.priority > 0
        elif self._axis == "y1":
            return self.tmpl.ymintic1.priority > 0
        elif self._axis == "y2":
            return self.tmpl.ymintic2.priority > 0

    @show_miniticks.setter
    def show_miniticks(self, val):
        """Use this attribute for the dict editor."""
        if self._axis == "x1":
            self.tmpl.xmintic1.priority = 1 if val else 0
        elif self._axis == "x2":
            self.tmpl.xmintic2.priority = 1 if val else 0
        elif self._axis == "y1":
            self.tmpl.ymintic1.priority = 1 if val else 0
        elif self._axis == "y2":
            self.tmpl.ymintic2.priority = 1 if val else 0

    @property
    def minitick_count(self):
        ticks = self.ticks
        if isinstance(ticks, str):
            ticks = vcs.elements["list"][ticks]
        axis_vals = sorted(ticks)
        mini_ticks = sorted(self.miniticks)

        last_val = axis_vals[0]
        between_ticks = -1
        for val in axis_vals[1:]:
            this_between = 0
            for i, tick in enumerate(mini_ticks):
                if tick > val:
                    mini_ticks = mini_ticks[i:]
                    break
                this_between += 1
            if between_ticks == -1:
                between_ticks = this_between
            if this_between != between_ticks:
                between_ticks = min(this_between, between_ticks)
            last_val = val
        return between_ticks

    @minitick_count.setter
    def minitick_count(self, count):
        ticks = self.ticks_as_dict()
        axis_vals = sorted(ticks)
        prev_val = axis_vals[0]
        miniticks = []
        for val in axis_vals[1:]:
            step = (val - prev_val) / float(count + 1)
            miniticks.extend((prev_val + step * i for i in range(count + 1)))
            prev_val = val
        self.miniticks = {t: "" for t in miniticks}

    def ticks_as_dict(self):
        ticks = self.ticks
        if isinstance(ticks, str):
            ticks = vcs.elements["list"][ticks]
        return ticks

    def save(self, name):
        vcs.elements["list"][name] = self.ticks
        vcs.elements["list"][name + "_miniticks"] = self.miniticks
