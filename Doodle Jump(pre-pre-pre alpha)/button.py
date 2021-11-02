from MODULES import *

from game_object import GameObject
from text_object import TextObject


class Button(GameObject):
    def __init__(self, x, y, w, h, text, on_click=lambda x: None, paddingX=0, paddingY=0):
        GameObject.__init__(self, x, y, w, h)
        self.state = 'normal'
        self.clicked = False
        self.on_click = on_click

        self.text = TextObject(x + paddingX, y + paddingY, lambda: text, c.button_text_color, c.font_name, c.font_size)

    @property
    def back_color(self):
        return dict(normal=c.button_normal_back_color,
                    hover=c.button_hover_back_color,
                    pressed=c.button_pressed_back_color,
                    pressed_once=c.button_pressed_back_color)[self.state]

    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color, self.bounds)
        self.text.draw(surface)

    def reset(self):
        self.clicked = False

    def handle_mouse_event(self, etype, pos):
        if etype == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif etype == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
            self.handle_mouse_click(pos)
        elif etype == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if self.bounds.collidepoint(pos):
            if self.state != "pressed":
                self.state = "hover"
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.on_click(self)
            self.state = 'hover'

    def handle_mouse_click(self, pos):
        if self.bounds.collidepoint(pos):
            self.clicked = True

    def reset_click(self):
        self.clicked = False

    def update(self):
        self.reset_click()

    def __del__(self):
        print("ID ", self.ID, " deleted button")


