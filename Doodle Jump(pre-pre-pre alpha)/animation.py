import pygame


class Animation:
    def __init__(self, animation_dict):
        self.animation = animation_dict["frames"]
        self.frames_count = animation_dict["frames_count"]
        self.ticks_skip = animation_dict["t_skip"]
        self.attach_obj = animation_dict["attach"]
        self.repeat_count = animation_dict["r_count"]
        self.offset = animation_dict["offset"]

        self.repeats = 0
        self.curr_frame = 0
        self.ticks_passed = 0

        self.disabled = False
        self.pause = False

        self.deleted = False

    def pause(self):
        self.pause = True

    def unpause(self):
        self.pause = False

    def disable(self):
        self.disabled = True
        self.curr_frame = 0

    def enable(self):
        self.disabled = False
        self.curr_frame = 0

    def draw(self, surface):
        if not self.disabled and not self.deleted:
            rect = self.attach_obj().rect.copy()
            rect.x += self.offset[0]
            rect.y += self.offset[1]
            surface.blit(self.animation[self.curr_frame],  rect)

            if not self.pause:
                if self.ticks_passed == self.ticks_skip:
                    self.curr_frame += 1
                    self.ticks_passed = 0
                else:
                    self.ticks_passed += 1

                if self.curr_frame == self.frames_count:
                    if self.repeat_count != -1:
                        self.curr_frame = 0
                        self.repeats += 1
                        if self.repeats >= self.repeat_count:
                            self.disable()
                    else:
                        self.curr_frame = 0

    def __del__(self):
        pass

