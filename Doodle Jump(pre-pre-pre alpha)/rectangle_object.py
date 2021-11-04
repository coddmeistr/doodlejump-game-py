import pygame.sprite

from MODULES import *

globals()["ID"] = 0


class RectObject:
    def __init__(self, x, y, w, h, speed=(0, 0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed

        self.ID = globals().get("ID")
        print("ID: ", self.ID)
        globals()["ID"] += 1

    @property
    def left(self):
        return self.rect.left

    @property
    def right(self):
        return self.rect.right

    @property
    def top(self):
        return self.rect.top

    @property
    def bottom(self):
        return self.rect.bottom

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    @property
    def center(self):
        return self.rect.center

    @property
    def centerx(self):
        return self.rect.centerx

    @property
    def centery(self):
        return self.rect.centery

    def draw(self, surface):
        pass

    def move(self, dx, dy):
        self.rect = self.rect.move(dx, dy)

    def update(self):
        if self.speed == [0, 0]:
            return

        self.move(*self.speed)

    def __del__(self):
        print("RECTANGLE OBJECT DELETED. UNDEFINED OBJECT, SOMETHING WRONG!")