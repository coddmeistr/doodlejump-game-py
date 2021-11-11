import pygame.sprite

from MODULES import *

globals()["ID"] = 0


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

        self.animations = []

        self.ID = globals().get("ID")
        # print("ID: ", self.ID)
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

    def add_anim(self, anim):
        self.animations.append(anim)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        for animation in self.animations:
            if animation is not None:
                animation().draw(surface)

    def move(self, dx, dy):
        self.rect = self.rect.move(dx, dy)

    def update(self):
        if self.speed == [0, 0]:
            return

        self.move(*self.speed)

    def __del__(self):
        print("GAME OBJECT DELETED. UNDEFINED OBJECT, SOMETHING WRONG!")
