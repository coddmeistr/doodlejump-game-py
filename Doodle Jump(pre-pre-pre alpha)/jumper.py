import pygame.sprite

from MODULES import *

from game_object import GameObject


class Jumper(GameObject):
    def __init__(self, x=0, y=0, offsetX=0):
        GameObject.__init__(self, x, y, "textures/jumper_front.png")

        # Moving states
        self.moving_left = False
        self.moving_right = False
        self.jumping_up = False
        self.jumping_down = True
        self.isCollision = False

        # Move params
        self.JUMP_DURATION = c.jump_duration
        self.JUMP_HEIGHT = c.jump_height
        self.offsetX = offsetX
        self.offsetY = 0

        # hidden jump's params
        self.last_height = self.JUMP_HEIGHT      # chasing previous height to increase it by delta
        self.func_a_coeff = self.find_a_coeff()  # "a" coeff in a jumping formula (ax^2 + c)
        self.time = 0                            # equals to "x" in a the jumping formula, changes with time
        self.last_dy = -1                        # previous delta height
        self.collision_dist = 1000               # this param store dist between jumper and collised platform

        # global game jumper's states
        self.game_over = False

        #debug
        self.prev_centery = self.centery

    # Find "a" coeff in a jumping formula ( ax^2 + c )
    def find_a_coeff(self):
        return -self.JUMP_HEIGHT / (self.JUMP_DURATION ** 2)

    # Finds the new Y offset via JUMP_HEIGHT and time(x)
    def offset_fun(self):
        new_height = self.func_a_coeff * (self.time**2) + self.JUMP_HEIGHT
        delta = abs(new_height - self.last_height)
        self.last_height = new_height + 0
        return delta

    # Handling buttons pressing
    def handle(self, key):
        if key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
        else:
            self.moving_right = not self.moving_right

    # Check collisions and returns platform if it was
    # Also setting collision_dist variable to the distance to this platform
    def collision_check(self, platforms):
        for p in platforms:
            if ((self.left <= p.left < self.right) or
                (p.left <= self.left and p.right >= self.right) or
                (self.right >= p.right >= self.left)) and\
                (p.top >= self.bottom) and\
                (abs(p.top-self.bottom) <= self.offsetY) and\
                    self.jumping_down:
                return p
        return None

    def jumper_death(self):
        self.game_over = True

    # Vertical moving(jumping)
    def jumping_move(self):
        if self.time >= 0 and self.jumping_up:
            self.jumping_up = False
            self.jumping_down = True
        if self.isCollision and self.jumping_down:
            self.time = -self.JUMP_DURATION
            self.last_height = 0
            self.jumping_up = True
            self.jumping_down = False
            self.collision_dist = 1000
            self.isCollision = False

        dy = 0
        self.offsetY = abs(self.offset_fun())
        if self.jumping_down:
            dy = min(self.offsetY, self.collision_dist)
        elif self.jumping_up:
            dy = -min(self.offsetY, self.centery - c.win_height / 2)
        self.last_dy = dy

        self.move(0, dy)

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

    def update(self):
        # Check lost condition
        if self.top > c.win_height:
            self.jumper_death()

        # Increase time via frame rate
        self.time += 1/c.framerate

        # Moving
        self.jumping_move()
        self.horizontal_move()

        #debug
        print(self.centery-self.prev_centery, " ", self.last_dy)
        self.prev_centery = self.centery

    def __del__(self):
        print("ID ", self.ID, " deleted JUMPER")
