import pygame.image
from game_object import GameObject
from delete import *
from animation_base import *


class Platform(GameObject):
    def __init__(self, x, y, base):
        GameObject.__init__(self, x, y, "textures/platform_basic.png")
        self.base = base

    def action(self):
        self.base.jumper.collision_dist = abs(self.top - self.base.jumper.bottom)
        self.base.jumper.isCollision = True
        self.base.sounds.play_sound("jump")

    def __del__(self):
        pass
        # print("ID ", self.ID, " deleted platform")


class MovingPlatform(GameObject):
    def __init__(self, x, y, speed, base):
        GameObject.__init__(self, x, y, "textures/platform_runic.png")
        self.base = base

        self.time = 0

        # random direction
        self.moving_left = random.choice([True, False])
        self.moving_right = not self.moving_left

        # values
        self.DUR = c.duration_moving_platforms()
        self.speed = speed

    def action(self):
        self.base.jumper.collision_dist = abs(self.top - self.base.jumper.bottom)
        self.base.jumper.isCollision = True
        self.base.sounds.play_sound("jump")

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
    def __init__(self, x, y, base):
        GameObject.__init__(self, x, y, "textures/platform_fake.png")
        self.base = base

        self.animation = base.anims.create_animation("dust_fall", weakref.ref(self), frame_rate=10,
                                                     offset=(0, 20))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.animation().draw(surface)

    def action(self):
        self.base.sounds.play_sound("fake_break")
        self.move(0, c.win_height)

    def __del__(self):
        pass
        #print("ID ", self.ID, " deleted platform(F)")


class AbsorbPlatform(GameObject):
    def __init__(self, x, y, base):
        GameObject.__init__(self, x, y, "textures/platform_fake.png")
        self.base = base

        # scenario stage of this platform action
        self.scenario_state = 0

        # time var
        self.time = 0

        # jumped jumper
        self.victim = None

        # fake jump params
        self.failed_speedY = 5
        self.failed_jump_height = 10
        self.failed_passed_height = 0

        # try jump params
        self.try_speedY = 10
        self.try_jump_height = 30
        self.try_passed_height = 0
        self.button_pressed = False

        self.time_to_death = 4.5
        self.clicks_to_escape = 10
        self.current_clicks = 0

    def action(self):
        self.base.jumper.collision_dist = abs(self.top - self.base.jumper.bottom)
        self.base.jumper.isCollision = True
        self.base.sounds.play_sound("jump")

        self.time = 0
        self.current_clicks = 0

        # Block jumper's move and give it's control to this platform
        self.victim = weakref.ref(self.base.jumper)
        self.victim().is_vertical_move = False
        self.victim().is_horizontal_move = False
        self.victim().collision_enabled = False

        # Handler for escape button
        self.base.keydown_handlers[pygame.K_UP].append(self.handle_button_event)

        # State
        self.scenario_state = 1

    def failed_jump_move(self):
        if self.failed_passed_height == self.failed_jump_height:
            self.failed_passed_height = 0
            self.scenario_state = 2
            return
        dy = -min(self.failed_speedY, self.failed_jump_height-self.failed_passed_height)
        self.victim().move(0, dy)
        self.failed_passed_height += abs(dy)

    def try_jump_move(self):
        if self.try_passed_height == self.try_jump_height:
            self.current_clicks += 1
            if self.current_clicks == self.clicks_to_escape:
                self.return_control()
                self.end_action_scene()
                self.try_passed_height = 0
                self.button_pressed = False
                return
            self.victim().move(0, self.try_passed_height)
            self.try_passed_height = 0
            self.button_pressed = False
            return
        dy = -min(self.try_speedY, self.try_jump_height - self.try_passed_height)
        self.victim().move(0, dy)
        self.try_passed_height += abs(dy)

    def handle_button_event(self, key):
        if self.scenario_state == 2:
            if key == pygame.K_UP:
                self.button_pressed = True

    def return_control(self):
        self.victim().is_vertical_move = True
        self.victim().is_horizontal_move = True
        self.victim().collision_enabled = True

    def end_action_scene(self):
        self.victim = None
        self.scenario_state = 0

    def time_track(self):
        self.time += 1/c.framerate
        if self.time >= self.time_to_death:
            self.scenario_state = 0
            self.victim().jumper_death()

    def update(self):
        if self.scenario_state == 1:
            self.failed_jump_move()
        elif self.scenario_state == 2:
            self.time_track()
            if self.button_pressed:
                self.try_jump_move()

    def __del__(self):
        pass
        # print("ID ", self.ID, " deleted platform(m)")


class SteinsPlatform(GameObject):
    def __init__(self, x, y, base):
        GameObject.__init__(self, x, y, "textures/platform_runic.png")

        self.scenario = 0

        self.base = base

    def action(self):
        self.base.jumper.isCollision = False

        self.base.movie.start_movie("steins_gate")

        self.base.jumper.steal_control()

        self.base.objects.remove(self)
        self.base.platforms.remove(self)
        delete_platforms(self.base)
        self.base.objects.append(self)
        self.base.platforms.append(self)

        platforms = self.base.pm.first_platforms_layer()
        for p in platforms:
            self.base.objects.append(p)
            self.base.platforms.append(p)

        self.scenario = 1

    def update(self):
        if self.scenario == 1:
            if not self.base.movie.play_movie:
                self.base.objects.remove(self)
                self.base.platforms.remove(self)
                self.base.jumper.full_randomize_move_state()
                self.base.jumper.return_control()

    def __del__(self):
        pass
        # print("ID ", self.ID, " deleted platform(m)")
