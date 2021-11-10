import math

import pygame.sprite

from MODULES import *

from game_object import GameObject


class Jumper(GameObject):
    def __init__(self, x=0, y=0, offset_x=0):
        GameObject.__init__(self, x, y, "textures/jumper_front.png")

        # Moving states
        self.moving_left = False
        self.moving_right = False
        self.jumping_up = False
        self.jumping_down = True

        self.collision_enabled = True
        self.isCollision = False

        self.is_vertical_move = True
        self.is_horizontal_move = True

        # Move params
        self.offsetX = offset_x
        self.offsetY = 0

        # speed params (vertical)
        self.jump_time = c.jump_time
        self.ticks = int(math.ceil(c.framerate * self.jump_time))
        self.ticks_passed = 0
        self.c = c.start_speed
        self.a = self.get_a(self.c, self.jump_time)
        self.x = -self.jump_time
        self.JUMP_HEIGHT = self.find_jump_height()

        # Exporting information
        self.last_dy = -1                        # previous delta height
        self.last_dx = -1
        self.collision_dist = 1000               # this param store dist between jumper and collised platform

        # global game jumper's states
        self.game_over = False

    def move(self, dx, dy):
        self.last_dy = dy
        self.last_dx = dx
        self.rect = self.rect.move(dx, dy)

    def find_jump_height(self):
        height = 0
        c_param = self.c
        a = self.get_a(self.c, self.jump_time)
        x = 0
        ticks_passed = 0
        while ticks_passed <= self.ticks:
            height += self.get_current_speed(a, x, c_param)
            x += 1/c.framerate
            ticks_passed += 1
        print("JUMP HEIGHT = ", height)
        return height

    # -c/(x1**2)
    @staticmethod
    def get_a(c_param, x1):
        return (-c_param) / (x1**2)

    @staticmethod
    def get_current_speed(a, x, c_param):
        return int(a * (x**2) + c_param)

    # Handling buttons pressing
    def handle(self, key):
        if key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
        else:
            self.moving_right = not self.moving_right

    # Check collisions and returns platform if it was
    # Also setting collision_dist variable to the distance to this platform
    def collision_check(self, platforms):
        if self.collision_enabled:
            for p in platforms:
                if ((self.left <= p.left < self.right) or
                    (p.left <= self.left and p.right >= self.right) or
                    (self.right >= p.right >= self.left)) and \
                        (p.top >= self.bottom) and \
                        (abs(p.top - self.bottom) <= self.offsetY) and \
                        self.jumping_down:
                    return p
        return None

    def jumper_death(self):
        self.game_over = True

    # Vertical moving(jumping)
    def jumping_move(self):
        if self.ticks_passed == self.ticks and self.jumping_up:
            self.jumping_up, self.jumping_down = False, True

            self.ticks_passed = 0
            self.x = -self.jump_time

        if self.isCollision and self.jumping_down:
            self.jumping_up, self.jumping_down = True, False
            self.collision_dist = 1000
            self.isCollision = False

            self.ticks_passed = 0
            self.x = 0

        dy = 0
        self.offsetY = self.get_current_speed(self.a, self.x, self.c)
        if self.jumping_down:
            dy = min(self.offsetY, self.collision_dist)
        elif self.jumping_up:
            dy = -min(self.offsetY, self.centery - c.win_height / 2)

        self.move(0, dy)
        self.ticks_passed += 1

        self.x += 1/c.framerate

    # Moving horizontal
    def horizontal_move(self):
        if self.moving_left:
            dx = -self.offsetX
        elif self.moving_right:
            dx = self.offsetX
        else:
            return

        self.move(dx, 0)
        if self.centerx <= 0:
            self.move(c.win_width, 0)
        if self.centerx >= c.win_width:
            self.move(-c.win_width, 0)

    # randomize move condition
    def full_randomize_move_state(self):
        self.jumping_up = True
        self.jumping_down = False
        x = random.random()
        self.x = x
        self.ticks_passed = int(math.ceil(c.framerate * self.x))
        self.rect.x = random.randint(0, c.win_width-20)
        self.rect.y = random.randint(c.win_height / 2, c.win_height - 20)

    def update(self):
        # Check lost condition
        if self.top > c.win_height:
            self.jumper_death()

        # Moving
        if self.is_vertical_move:
            self.jumping_move()
        if self.is_horizontal_move:
            self.horizontal_move()

    def __del__(self):
        print("ID ", self.ID, " deleted JUMPER")
