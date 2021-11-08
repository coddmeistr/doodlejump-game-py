
from MODULES import *

from rectangle_object import RectObject
from button_sprite import ButtonSprite


def create_scroller(self, x, y, param, handler, bounds, w=200, h=100, rect_color=colors.GRAY40, blocked=()):
    scroller = Scroller(x, y, w, h, param, handler, bounds, rect_color, blocked_elems=blocked)
    self.mouse_handlers.append(scroller.slider.handle_mouse_event)
    self.mouse_handlers.append(scroller.rect_back.handle_mouse_event)
    self.objects.append(scroller)


class Scroller:
    def __init__(self, x, y, w, h, param, handler, bounds, rect_color, blocked_elems):
        if bounds[0] > bounds[1]:
            raise Exception("Scroller's invalid bounds")

        self.rect_back = Rectangle(x, y, w, h, rect_color)
        w_l, h_l = w/1.2, h/10
        x_l, y_l = x + (w - w_l)/2, y + (h - h_l)/2
        self.rect_line = Rectangle(x_l, y_l, w_l, h_l, colors.BLACK)

        curr_x = (param / bounds[1])*self.rect_line.width
        x_s, y_s = x_l+curr_x, y_l - h_l/2 - 3  # Change x here. Also -3 just fixing texture(don't know why it not good)
        self.slider = Slider(x_s, y_s)
        self.slider.rect.x -= self.slider.width/2

        self.param = param
        self.bounds = bounds
        self.handler = handler
        self.blocked_elems = blocked_elems

    def draw(self, surface):
        self.rect_back.draw(surface)
        self.rect_line.draw(surface)
        self.slider.draw(surface)

    def delete_cond(self):
        return self.rect_back.delete_scroller_state

    def update(self):
        if self.slider.state == "pressed":
            dist = self.slider.cursor_pos[0] - self.slider.centerx
            if dist < 0:
                dx = -min(abs(dist), abs(self.rect_line.left-self.slider.centerx))
            elif dist > 0:
                dx = min(dist, self.rect_line.right-self.slider.centerx)
            else:
                dx = 0

            self.slider.move(dx, 0)
            self.param = ((self.slider.centerx - self.rect_line.left)/self.rect_line.width) * \
                         (self.bounds[1]-self.bounds[0])
            self.handler(self.param)

    def __del__(self):
        del self.param
        del self.bounds
        del self.handler


class Slider(ButtonSprite):
    def __init__(self, x, y):
        ButtonSprite.__init__(self, x, y, "", "textures/polzunok.png", "textures/polzunok.png",
                              "textures/polzunok.png")

        self.cursor_pos = 0

    def handle_mouse_move(self, pos):
        self.cursor_pos = pos
        if self.state == "pressed":
            return
        if self.rect.collidepoint(pos):
            self.state = "hover"
        else:
            self.state = "normal"

    def handle_mouse_down(self, pos):
        if self.rect.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed' and self.rect.collidepoint(pos):
            self.state = 'hover'
        else:
            self.state = "normal"


class Rectangle(RectObject):
    def __init__(self, x, y, w, h, color):
        RectObject.__init__(self, x, y, w, h)
        self.color = color

        self.delete_scroller_state = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,  self.rect)

    def handle_mouse_event(self, etype, pos):
        if etype == pygame.MOUSEBUTTONDOWN:
            self.handle_exit_mouse(pos)

    def handle_exit_mouse(self, pos):
        if not self.rect.collidepoint(pos):
            self.delete_scroller_state = True

    def __del__(self):
        pass
        # print("ID ", self.ID, " deleted Rectangle")
