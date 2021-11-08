import pygame.image

from MODULES import *

from game_object import GameObject


class Platform(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, x, y, "textures/platform_basic.png")

    def __del__(self):
        pass
        # print("ID ", self.ID, " deleted platform")


class MovingPlatform(GameObject):
    def __init__(self, x, y, speed):
        GameObject.__init__(self, x, y, "textures/platform_runic.png")

        self.time = 0

        # random direction
        self.moving_left = random.choice([True, False])
        self.moving_right = not self.moving_left

        # values
        self.DUR = c.duration_moving_platforms()
        self.speed = speed

    def offset_fun(self):
        return self.speed

    def move_horizontal(self):
        if self.time >= self.DUR and self.moving_left:
            self.moving_left = False
            self.moving_right = True
            self.time = 0
        if self.time >= self.DUR and self.moving_right:
            self.moving_left = True
            self.moving_right = False
            self.time = 0

        dx = abs(self.offset_fun())
        if self.moving_left:
            dx = -min(dx, self.left)
        else:
            dx = min(dx, c.win_width - self.right)

        self.move(dx, 0)

    def update(self):
        self.time += 1/c.framerate

        self.move_horizontal()

    def __del__(self):
        pass
        # print("ID ", self.ID, " deleted platform(m)")


class FakePlatform(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, x, y, "textures/platform_fake.png")

        # DUST FALL ANIMATION
        self.dust_fall_animation = [pygame.image.load("textures/animation_fake_platform/pyl1.png").convert_alpha(),
                                    pygame.image.load("textures/animation_fake_platform/pyl2.png").convert_alpha(),
                                    pygame.image.load("textures/animation_fake_platform/pyl3.png").convert_alpha(),
                                    pygame.image.load("textures/animation_fake_platform/pyl4.png").convert_alpha(),
                                    pygame.image.load("textures/animation_fake_platform/pyl5.png").convert_alpha(),
                                    pygame.image.load("textures/animation_fake_platform/pyl6.png").convert_alpha(),
                                    pygame.image.load("textures/animation_fake_platform/pyl7.png").convert_alpha()]
        self.anim_count = 0
        self.FPS = 60
        self.ticks_passed = 0
        self.skip_ticks = int(1/(self.FPS / c.framerate))-1
        self.is_draw_animation = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.is_draw_animation:
            rect = self.rect.copy()
            rect.y += rect.height - 30
            surface.blit(self.dust_fall_animation[self.anim_count // 8], rect)

            if self.anim_count + 1 > 49 and self.ticks_passed == self.skip_ticks:
                self.anim_count = 0
                self.ticks_passed = 0
            elif self.ticks_passed == self.skip_ticks:
                self.anim_count += 1
                self.ticks_passed = 0
            else:
                self.ticks_passed += 1

        elif self.is_draw_animation:
            self.ticks_passed += 1

    def __del__(self):
        pass
        # print("ID ", self.ID, " deleted platform(m)")
