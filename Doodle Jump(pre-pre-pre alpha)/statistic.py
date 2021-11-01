from MODULES import *

from text_object import TextObject
from game_object import GameObject


class Statistic(TextObject, GameObject):
    def __init__(self, x, y, text_func, color, font_name, font_size):
        super().__init__(x, y, text_func, color, font_name, font_size)
        self.param = 0
        self.text = text_func()

    def update(self):
        self.text_func = lambda: self.text+": "+str(int(self.param))

    def __del__(self):
        print("stats tracker deleted")
