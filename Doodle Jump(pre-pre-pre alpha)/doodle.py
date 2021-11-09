import pygame.mixer_music

import jumper

from game_object import *
from centralizer import *
from delete import *
from game import Game
from jumper import Jumper
from text_object import TextObject
from button import Button
from statistic import Statistic
from scroller import *


class Doodle(Game):
    def __init__(self):
        Game.__init__(self, 'Doodle Jump', c.win_width, c.win_height, "images/background.jpg", c.framerate)

        self.jumper = Jumper()

        # Background moving
        self.height_passed = 0
        self.height_to_one_pixel_move = 1000

        # Time trackers(for any events)
        self.time = 0  # Main time tracker
        self.game_lost_time = -1

        # Game statistic
        self.points_text = None
        self.jumped_platforms_count_text = None
        self.max_height_text = None

        # Init actions(create menu, set game over var, set music, set game state)
        self.game_over = False
        self.game_state = 'Menu_main'
        self.music.set_music_theme("menu")
        self.create_menu()

    def create_menu(self):
        main_menu_buttons = list()

        text, w, h, px, py = get_centralized_params(self.font, "ИГРАТЬ", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 150, w, h, text, padding_x=px, padding_y=py))
        text, w, h, px, py = get_centralized_params(self.font, "НАСТРОЙКИ", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 250, w, h, text, padding_x=px, padding_y=py))
        text, w, h, px, py = get_centralized_params(self.font, "ВЫХОД", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 350, w, h, text, padding_x=px, padding_y=py))
        for button in main_menu_buttons:
            self.mouse_handlers.append(button.handle_mouse_event)
            self.objects.append(button)
            self.buttons.append(button)

    def create_menu_settings(self):
        main_menu_buttons = list()

        text, w, h, px, py = get_centralized_params(self.font, "ЗВУКИ", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 100, w, h, text, padding_x=px, padding_y=py))
        print(w, h)
        text, w, h, px, py = get_centralized_params(self.font, "МУЗЫКА", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 200, w, h, text, padding_x=px, padding_y=py))
        text, w, h, px, py = get_centralized_params(self.font, "СЛОЖНОСТЬ", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 300, w, h, text, padding_x=px, padding_y=py))
        text, w, h, px, py = get_centralized_params(self.font, "НАЗАД", 7, 7)
        main_menu_buttons.append(Button(c.win_width / 2 - w / 2, 400, w, h, text, padding_x=px, padding_y=py))
        for button in main_menu_buttons:
            self.mouse_handlers.append(button.handle_mouse_event)
            self.objects.append(button)
            self.buttons.append(button)

    def create_jumper(self):
        jumper_obj = Jumper(c.win_width / 2, c.win_height / 2 - 15, c.jumper_speedX)
        self.keydown_handlers[pygame.K_LEFT].append(jumper_obj.handle)
        self.keydown_handlers[pygame.K_RIGHT].append(jumper_obj.handle)
        self.keyup_handlers[pygame.K_LEFT].append(jumper_obj.handle)
        self.keyup_handlers[pygame.K_RIGHT].append(jumper_obj.handle)
        self.jumper = jumper_obj

        self.objects.append(self.jumper)

    def create_stats_trackers(self):
        self.max_height_text = Statistic(3, 0, lambda: "height", colors.BLUE, c.font_name, c.font_size_trackers)
        self.points_text = Statistic(3, 30, lambda: "points", colors.BLUE, c.font_name, c.font_size_trackers)
        self.jumped_platforms_count_text = Statistic(3, 60, lambda: "jumps", colors.BLUE, c.font_name,
                                                     c.font_size_trackers)
        self.objects.append(self.max_height_text)
        self.objects.append(self.points_text)
        self.objects.append(self.jumped_platforms_count_text)

    def game_lost(self):
        # create basic GameObject to display "GAME LOST!"
        game_lost_text = GameObject(c.win_width / 2 - 75, c.win_height / 2 - 150, "textures/you_lost.png")

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
        #self.multicolor.add_object(weakref.ref(game_lost_text), left_color=(0, 0, 255), right_color=(255, 0, 0))
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
            delete_objects(self)
            self.music.set_music_theme("menu")
            self.background.change_background_menu("default")
            self.create_menu()
            self.game_state = "Menu_main"
            self.game_lost_time = -1

    def camera_chasing(self):
        if self.jumper.jumping_up:
            change = self.jumper.offsetY - abs(self.jumper.last_dy)
            for o in self.objects:
                if not isinstance(o, jumper.Jumper):
                    o.move(0, change)
                    self.pm.last_platform_height -= change
            return change+0  # returns height change (high)
        return 0

    def update_points(self, height_delta, is_jumped):
        if is_jumped:
            d = 1
        else:
            d = 0
        self.max_height_text.param += height_delta
        self.jumped_platforms_count_text.param += d
        self.points_text.param += height_delta / 10 + d * 100

    def clean_garbage(self):
        for o in self.objects_to_remove:
            self.objects.remove(o)
        self.objects_to_remove = []

    def update(self):
        self.time += 1 / c.framerate

        # STATES HANDLERS HERE
        # STATES HANDLERS HERE
        if self.game_state == "Menu_main":
            self.main_menu_handler()

        if self.game_state == "Play":
            self.playing_game_handler()

        if self.game_state == "Menu_settings":
            self.menu_settings_handler()
        # STATES HANDLERS HERE(UP)
        # STATES HANDLERS HERE(UP)

        # other objects manipulations
        self.multicolor.update()
        # generic objects manipulation
        for o in self.objects:
            o.update()

            if self.game_state == "Menu_settings":
                # try to delete scroller
                try:
                    if o.delete_cond():
                        for elem in o.blocked_elems:
                            elem.enable()
                        self.objects_to_remove.append(o)
                        self.mouse_handlers.remove(o.slider.handle_mouse_event)
                        self.mouse_handlers.remove(o.rect_back.handle_mouse_event)
                except AttributeError:
                    self.errors_log[AttributeError] += "doodle.py: update(): for o in self.objects:...\n"
                except BaseException:
                    raise RuntimeError("UNKNOWN UNHANDLED ERROR: doodle.py: for o in self.objects:...\n")

            # delete movable object, IF HE IS LOWER THAT c.win_height + 10
            if self.game_state == "Play":
                try:
                    # No exception if object is movable
                    if o.top > c.win_height + 10 and not isinstance(o, jumper.Jumper):
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

    # GAME STATES HANDLERS HERE. EVERY GAME STATE IS HANDLING HERE
    # game_state == Menu_main
    def main_menu_handler(self):
        if self.buttons[0].state == "pressed":
            delete_objects(self)
            self.pm.last_platform_height = 0

            # Create jumper. Add jumped to Platform Manager and create statistic trackers
            self.create_jumper()
            self.pm.jumper = weakref.ref(self.jumper)  # add jumper to pm
            self.create_stats_trackers()
            # Create plato and the first layer of platforms
            plato = self.pm.create_plato()
            platforms = self.pm.first_platforms_layer()
            for p in plato + platforms:
                self.objects.append(p)
                self.platforms.append(p)
            # Set play music theme and background
            self.music.set_music_theme("play")
            self.background.change_background_game("level_1")
            # Set the game state to - Play
            self.game_over = False
            self.game_state = "Play"
            return

        # Settings
        if self.buttons[1].state == "pressed":
            delete_objects(self)

            self.create_menu_settings()

            self.game_state = "Menu_settings"

        # Exit
        if self.buttons[2].state == "pressed":
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

    # game_state == Play
    def playing_game_handler(self):
        if not self.game_over:
            plat = self.jumper.collision_check(self.platforms)
            is_jumped = False
            if plat is not None:
                # temporary line, it fixes collision bug, not it's ok
                self.jumper.move(0, plat.top - self.jumper.bottom)

                is_jumped = True
                # Jumped platform height
                self.pm.jumped_platform_height = plat.height
                # Create save platform on the next layer
                save_plat = self.pm.create_saving_platform()
                self.objects.append(save_plat)
                self.platforms.append(save_plat)
                # Do jump action of a platform
                plat.action(self)

            # Chasing height diff.
            height_dif = self.camera_chasing()

            # Background moving
            self.height_passed += height_dif
            if self.height_passed >= self.height_to_one_pixel_move:
                self.background.change_offset(0, 1)
                self.height_passed -= self.height_to_one_pixel_move

            # Update points
            self.update_points(height_dif, is_jumped)

            # If tracking platform(highest platform of the last layer) is displayed
            # Then create a new layer
            if self.pm.tracking_platform.top >= 0:
                platforms = self.pm.another_platforms()
                for p in platforms:
                    self.objects.append(p)
                    self.platforms.append(p)

            # If jumper is lost
            if self.jumper.game_over:
                # delete jumper
                delete_jumper(self.keyup_handlers, self.keydown_handlers, self.jumper, self.errors_log)
                self.objects.remove(self.jumper)
                self.jumper = None
                # action
                self.game_lost()
                self.game_lost_time = self.time + 0
                self.game_over = True
        else:
            self.game_lost_pause()

    # game_state == Menu_settings
    def menu_settings_handler(self):
        # Sound
        if self.buttons[0].clicked:

            # volume scroller creation
            blocked = []
            for button in self.buttons:
                button.disable()
                blocked.append(button)
            w, h = 200, 100
            create_scroller(self, self.buttons[0].right + 50, self.buttons[0].top - 25,
                            self.sounds.volume, self.sounds.change_volume,
                            [0, 1],
                            w=w, h=h,
                            blocked=blocked)

        # Music
        if self.buttons[1].clicked:

            # volume scroller creation
            blocked = []
            for button in self.buttons:
                button.disable()
                blocked.append(button)
            w, h = 200, 100
            create_scroller(self, self.buttons[1].right + 50, self.buttons[1].top - 25,
                            self.music.volume, self.music.change_volume,
                            [0, 1],
                            w=w, h=h,
                            blocked=blocked)

        # Difficulty
        if self.buttons[2].clicked:
            pass

        # Back
        if self.buttons[3].state == "pressed":
            delete_objects(self)

            self.create_menu()

            self.game_state = "Menu_main"


def main():
    Doodle().run()


if __name__ == '__main__':
    main()
