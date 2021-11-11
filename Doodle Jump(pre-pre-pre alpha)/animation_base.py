import weakref

import pygame
import os
import config as c
from animation import Animation


class AnimationBase:
    def __init__(self):
        self.animations = {"dust_fall": self.load_animation("animations/dust_fall"),
                           "rotating_gear": self.load_animation("animations/rotating_gear")
                      }

        self.on_draw_animations = []

    @staticmethod
    def load_animation(storage):
        animation = []
        for subdir, dirs, files in os.walk(storage):
            for file in files:
                animation.append(pygame.image.load(os.path.join(subdir, file)).convert_alpha())
        return animation

    def create_animation(self, tag, attach_obj, repeat_count=-1, frame_rate=c.framerate, offset=(0, 0)):
        animation = dict()
        animation["frames"] = self.animations[tag]
        animation["frames_count"] = len(self.animations[tag])
        animation["attach"] = attach_obj
        animation["t_skip"] = int(1/(frame_rate / c.framerate))
        animation["offset"] = offset
        if repeat_count == -1:
            animation["r_count"] = -1
        elif repeat_count >= 0:
            animation["r_count"] = repeat_count
        else:
            raise Exception
        new_anim = Animation(animation)
        self.on_draw_animations.append(new_anim)
        return weakref.ref(new_anim)

    def update(self):
        for animation in self.on_draw_animations:
            if animation.attach_obj() is None:
                self.on_draw_animations.remove(animation)
