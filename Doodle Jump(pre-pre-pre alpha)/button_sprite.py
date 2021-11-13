import pygame.image

from MODULES import *

from game_object import GameObject
from text_object import TextObject


class ButtonSprite(GameObject):
    def __init__(self, x, y, text, normal, hover, pressed, padding_x=0, padding_y=0):
        self.states_textures = {"normal": normal,
                                "hover": hover,
                                "pressed": pressed}
        GameObject.__init__(self, x, y, self.states_textures["normal"])

        self.state = 'normal'
        self.clicked = False
        self.disabled = False

        self.text = TextObject(x + padding_x, y + padding_y, lambda: text, c.button_text_color,
                               c.font_name, c.font_size)

    def draw(self, surface):
        surface.blit(self.button_texture, self.rect)

        for animation in self.animations:
            if animation is not None:
                animation().draw(surface)

    @property
    def button_texture(self):
        return dict(normal=self.states_textures["normal"],
                    hover=self.states_textures["hover"],
                    pressed=self.states_textures["pressed"])[self.state]

    def reset(self):
        self.clicked = False

    def handle_mouse_event(self, etype, pos):
        if not self.disabled:
            if etype == pygame.MOUSEMOTION:
                self.handle_mouse_move(pos)
            elif etype == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(pos)
                self.handle_mouse_click(pos)
            elif etype == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if self.rect.collidepoint(pos):
            if self.state != "pressed":
                self.state = "hover"
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.rect.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.state = 'hover'

    def handle_mouse_click(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked = True

    def reset_click(self):
        self.clicked = False

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False

    def update(self):
        self.reset_click()

    def __del__(self):
        pass
        # print("ID ", self.ID, " deleted button")
