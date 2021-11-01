from MODULES import *

globals()["ID"] = 0


class GameObject:
    def __init__(self, x, y, w, h, speed=(0, 0)):
        self.ID = globals().get("ID")
        print("ID: ", self.ID)
        globals()["ID"] += 1

        self.bounds = pygame.Rect(x, y, w, h)
        self.speed = speed

    @property
    def left(self):
        return self.bounds.left

    @property
    def right(self):
        return self.bounds.right

    @property
    def top(self):
        return self.bounds.top

    @property
    def bottom(self):
        return self.bounds.bottom

    @property
    def width(self):
        return self.bounds.width

    @property
    def height(self):
        return self.bounds.height

    @property
    def center(self):
        return self.bounds.center

    @property
    def centerx(self):
        return self.bounds.centerx

    @property
    def centery(self):
        return self.bounds.centery

    def rectangle(self):
        return pygame.Rect(self.bounds.left, self.bounds.top, self.width, self.height)

    def draw(self, surface):
        pass

    def move(self, dx, dy):
        self.bounds = self.bounds.move(dx, dy)

    def update(self):
        if self.speed == [0, 0]:
            return

        self.move(*self.speed)

    def __del__(self):
        print("GAME OBJECT DELETED. UNDEFINED OBJECT, SOMETHING WRONG!")
