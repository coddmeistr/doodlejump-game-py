from text_object import TextObject


class Statistic(TextObject):
    def __init__(self, x, y, text_func, color, font_name, font_size):
        TextObject.__init__(self, x, y, text_func, color, font_name, font_size)
        self.param = 0
        self.text = text_func()

    def update(self):
        self.text_func = lambda: self.text+": "+str(int(self.param))

    def __del__(self):
        pass
        # print("stats tracker deleted")
