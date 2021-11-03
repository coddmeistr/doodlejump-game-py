from MODULES import *

from centralizer import *
from states_handlers import *
from delete import *
from game import Game
from jumper import Jumper
from platform import random_platform
from text_object import TextObject
from button import Button
from statistic import Statistic


class Doodle(Game):
    def __init__(self):
        Game.__init__(self, 'Doodle Jump', c.win_width, c.win_height, "images/background.jpg", c.framerate)

        self.jumper = Jumper()

        # Time trackers(for any events)
        self.time = 0  # Main time tracker
        self.game_lost_time = -1

        # platforms creation
        self.last_platform_height = 0
        self.tracking_platform = None

        # Game states
        self.game_over = False
        self.game_state = 'Menu_main'

        self.music.set_music_theme("menu")
        self.create_menu()

        # Game statistic
        self.points_text = None
        self.jumped_platforms_count_text = None
        self.max_height_text = None

    def create_menu(self):
        main_menu_buttons = list()

        text, w, h, px, py = get_centralized_params(self.font, "ИГРАТЬ", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 150, w, h, text, paddingX=px, paddingY=py))
        text, w, h, px, py = get_centralized_params(self.font, "НАСТРОЙКИ", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 250, w, h, text, paddingX=px, paddingY=py))
        text, w, h, px, py = get_centralized_params(self.font, "ВЫХОД", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 350, w, h, text, paddingX=px, paddingY=py))
        for button in main_menu_buttons:
            self.mouse_handlers.append(button.handle_mouse_event)
            self.objects.append(button)
            self.buttons.append(button)

    def create_menu_settings(self):
        main_menu_buttons = list()

        text, w, h, px, py = get_centralized_params(self.font, "ЗВУКИ: " + str(self.volume_sounds), 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 100, w, h, text, paddingX=px, paddingY=py))
        text, w, h, px, py = get_centralized_params(self.font, "МУЗЫКА: " + str(self.volume_music), 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 200, w, h, text, paddingX=px, paddingY=py))
        text, w, h, px, py = get_centralized_params(self.font, "СЛОЖНОСТЬ", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 300, w, h, text, paddingX=px, paddingY=py))
        text, w, h, px, py = get_centralized_params(self.font, "НАЗАД", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 400, w, h, text, paddingX=px, paddingY=py))
        for button in main_menu_buttons:
            self.mouse_handlers.append(button.handle_mouse_event)
            self.objects.append(button)
            self.buttons.append(button)

    def create_jumper(self):
        jumper = Jumper(c.win_width / 2, c.win_height / 2 - 15, 20, 30, c.jumper_speedX)
        self.keydown_handlers[pygame.K_LEFT].append(jumper.handle)
        self.keydown_handlers[pygame.K_RIGHT].append(jumper.handle)
        self.keyup_handlers[pygame.K_LEFT].append(jumper.handle)
        self.keyup_handlers[pygame.K_RIGHT].append(jumper.handle)
        self.jumper = jumper

        self.objects.append(self.jumper)

    def first_platforms_layer(self):
        max_platform_distance = 0
        if self.jumper.JUMP_DURATION * c.framerate * self.jumper.offsetX >= c.win_width / 2:
            max_platform_distance = self.jumper.JUMP_HEIGHT + 0
        else:
            pass

        heights = list()
        for _ in range(random.randint(13, 30)):
            heights.append(random.randint(0, max_platform_distance))
        heights.append(random.randint(c.win_height, c.win_height + 100))
        maximum_height = max(heights)

        width = 40
        long = 5
        platforms = []
        heights.sort()
        for h in heights:
            platform = random_platform(random.randint(0, c.win_width - width),
                                       c.win_height - h, width, long, [0, 100])
            platforms.append(platform)
            heights.remove(h)

        self.tracking_platform = platforms[-1]
        for platform in platforms:
            self.platforms.append(platform)
            self.objects.append(platform)

        self.last_platform_height = maximum_height

    def another_platforms(self):
        max_platform_distance = 0
        if self.jumper.JUMP_DURATION * c.framerate * self.jumper.offsetX >= c.win_width / 2:
            max_platform_distance = self.jumper.JUMP_HEIGHT + 0
        else:
            pass

        heights = list()
        for _ in range(random.randint(13, 30)):
            heights.append(random.randint(c.win_height, c.win_height + max_platform_distance))
        maximum_height = max(heights)

        width = 40
        long = 5
        platforms = []
        heights.sort()
        for h in heights:
            platform = random_platform(random.randint(0, c.win_width - width),
                                       c.win_height - h, width, long, [70, 10, 20])
            platforms.append(platform)
            heights.remove(h)

        self.tracking_platform = platforms[-1]
        for platform in platforms:
            self.platforms.append(platform)
            self.objects.append(platform)

        self.last_platform_height = maximum_height

    def create_plato(self):
        for i in range(0, c.win_width // 40):
            platform = random_platform(i * 40, c.win_height - 5, 40, 5, [100, 0])
            self.platforms.append(platform)
            self.objects.append(platform)

    def create_stats_trackers(self):
        self.max_height_text = Statistic(3, 0, lambda: "height", colors.BLUE, c.font_name, c.font_size_trackers)
        self.points_text = Statistic(3, 30, lambda: "points", colors.BLUE, c.font_name, c.font_size_trackers)
        self.jumped_platforms_count_text = Statistic(3, 60, lambda: "jumps", colors.BLUE, c.font_name,
                                                     c.font_size_trackers)
        self.objects.append(self.max_height_text)
        self.objects.append(self.points_text)
        self.objects.append(self.jumped_platforms_count_text)

    def game_lost(self):
        # create basic TextObject to display "GAME LOST!"
        temp_font = pygame.font.Font(c.font_name, 50)
        text = "GAME LOST!"
        game_lost_text = TextObject(c.win_width / 2 - temp_font.size(text)[0] / 2, c.win_height / 2 - 60,
                                    lambda: text, colors.RED1, c.font_name, 50)
        # save params
        height = self.max_height_text.param + 0
        points = self.points_text.param + 0
        platforms = self.jumped_platforms_count_text.param + 0
        # remove and delete old statistic
        self.objects.remove(self.jumped_platforms_count_text)
        self.objects.remove(self.points_text)
        self.objects.remove(self.max_height_text)
        delete_trackers([self.points_text, self.jumped_platforms_count_text, self.max_height_text], self.errors_log)
        self.jumped_platforms_count_text = None
        self.points_text = None
        self.max_height_text = None
        # create new statistic
        temp_font = pygame.font.Font(c.font_name, 30)
        text1 = "height: " + str(int(height))
        self.max_height_text = TextObject(c.win_width / 2 - temp_font.size(text1)[0] / 2, c.win_height / 2 - 15,
                                          lambda: text1, colors.ORANGE, c.font_name, 30)
        text2 = "points: " + str(int(points))
        self.points_text = TextObject(c.win_width / 2 - temp_font.size(text2)[0] / 2, c.win_height / 2 + 20,
                                      lambda: text2, colors.ORANGE, c.font_name, 30)
        text3 = "jumps: " + str(int(platforms))
        self.jumped_platforms_count_text = TextObject(c.win_width / 2 - temp_font.size(text3)[0] / 2,
                                                      c.win_height / 2 + 55,
                                                      lambda: text3, colors.ORANGE, c.font_name, 30)
        # add to multi coloring
        self.multicolor.add_object(weakref.ref(game_lost_text), left_color=(0, 0, 255), right_color=(255, 0, 0))
        self.multicolor.add_object(weakref.ref(self.max_height_text), left_color=(0, 0, 255), right_color=(255, 0, 0))
        self.multicolor.add_object(weakref.ref(self.points_text), left_color=(0, 0, 255), right_color=(255, 0, 0))
        self.multicolor.add_object(weakref.ref(self.jumped_platforms_count_text), left_color=(0, 0, 255),
                                   right_color=(255, 0, 0))
        # add them to the objects
        self.objects.append(game_lost_text)  # basic TextObject
        self.objects.append(self.jumped_platforms_count_text)
        self.objects.append(self.points_text)
        self.objects.append(self.max_height_text)

    def game_lost_pause(self):
        if self.game_lost_time < 0:
            return
        time_elapsed = self.time - self.game_lost_time
        if time_elapsed >= c.after_lost_pause:
            self.delete_objects()
            self.music.set_music_theme("menu")
            self.create_menu()
            self.game_state = "Menu_main"
            self.game_lost_time = -1

    def camera_chasing(self):
        if self.jumper.centery < c.win_height / 2 and self.jumper.last_dy < 0:
            for o in self.objects:
                o.move(0, -self.jumper.last_dy)
            self.last_platform_height -= self.jumper.last_dy
            return -self.jumper.last_dy  # returns height change (high)
        return 0

    def update_points(self, height_delta, jumped_plat):
        self.max_height_text.param += height_delta
        self.jumped_platforms_count_text.param += jumped_plat
        self.points_text.param += height_delta / 10 + jumped_plat * 100

    def delete_objects(self):
        # delete platforms
        self.tracking_platform = None
        for o in self.platforms:
            del o
        # delete buttons
        for o in self.buttons:
            self.mouse_handlers.remove(o.handle_mouse_event)
            del o
        # delete all objects
        for o in self.objects:
            del o
        # to default lists
        self.objects = []
        self.platforms = []
        self.buttons = []
        # delete all jumper handlers and jumper
        delete_jumper(self.keyup_handlers, self.keydown_handlers, self.jumper, self.errors_log)
        self.jumper = None
        # delete all statistic trackers
        delete_trackers([self.points_text, self.max_height_text, self.jumped_platforms_count_text], self.errors_log)
        self.points_text = None
        self.jumped_platforms_count_text = None
        self.max_height_text = None

    def clean_garbage(self):
        for o in self.objects_to_remove:
            self.objects.remove(o)
        self.objects_to_remove = []

    def update(self):
        self.time += 1 / c.framerate

        # STATES HANDLERS HERE
        # STATES HANDLERS HERE
        if self.game_state == "Menu_main":
            main_menu_handler(self)

        if self.game_state == "Play":
            playing_game_handler(self)

        if self.game_state == "Menu_settings":
            menu_settings_handler(self)
        # STATES HANDLERS HERE(UP)
        # STATES HANDLERS HERE(UP)

        # other objects manipulations
        self.multicolor.update()
        # generic objects manipulation
        for o in self.objects:
            o.update()

            # delete movable object, IF HE IS LOWER THAT c.win_height + 10
            if self.game_state == "Play":
                try:
                    # No exception if object is movable
                    if o.top > c.win_height + 10:
                        # it will be deleted at the end of a tick
                        self.objects_to_remove.append(o)
                        # The list of objects collections that you want to delete here (START)
                        try_delete_object_by_id(self.platforms, o.ID)  # try to delete platform
                        # (END)
                        del o
                except AttributeError:
                    self.errors_log[AttributeError] += "doodle.py: update(): for o in self.objects:...\n"
                except BaseException:
                    raise RuntimeError("UNKNOWN UNHANDLED ERROR: doodle.py: for o in self.objects:...\n")
        # Cleaning deleted objects from self.objects
        self.clean_garbage()


def main():
    Doodle().run()


if __name__ == '__main__':
    main()
