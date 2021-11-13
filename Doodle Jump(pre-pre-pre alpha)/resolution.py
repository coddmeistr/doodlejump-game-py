import config as c


class Resolution:
    def __init__(self, w, h):
        self.wnd_w = w
        self.wnd_h = h

    def get_scale(self, scale):
        return tuple([scale[0] * self.wnd_w / c.win_width, scale[1] * self.wnd_h / c.win_height])
