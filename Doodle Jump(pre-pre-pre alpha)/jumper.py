from MODULES import *

from game_object import GameObject


class Jumper(GameObject):
    def __init__(self, x=0, y=0, w=0, h=0, offsetX=0):
        GameObject.__init__(self, x, y, w, h)

        # Jumper's texture
        self.texture = pygame.image.load("textures/jumper_front.png")

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

                self.collision_dist = abs(p.top-self.bottom)
                self.isCollision = True
                return p
        return None

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
            dy = -self.offsetY
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
            self.game_over = True

        # Increase time via frame rate
        self.time += 1/c.framerate

        # Moving
        self.jumping_move()
        self.horizontal_move()

    def draw(self, surface):
        # pygame.draw.rect(surface, self.color, self.bounds) # not necessary
        surface.blit(self.texture, self.bounds)

    def __del__(self):
        print("ID ", self.ID, " deleted JUMPER")
