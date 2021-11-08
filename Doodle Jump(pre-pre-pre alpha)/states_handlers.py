from delete import *
import platform
from music_sounds import *
from scroller import *
from itertools import zip_longest


# game_state == Menu_main
def main_menu_handler(self):
    if self.buttons[0].state == "pressed":
        delete_objects(self)
        self.pm.last_platform_height = 0

        self.create_jumper()
        self.pm.jumper = weakref.ref(self.jumper)  # add jumper to pm
        self.create_stats_trackers()

        plato = self.pm.create_plato()
        platforms = self.pm.first_platforms_layer()
        for p in plato+platforms:
            self.objects.append(p)
            self.platforms.append(p)

        self.music.set_music_theme("play")
        self.background.change_background_game("level_1")

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
        plat_was_jumped = 0
        plat = self.jumper.collision_check(self.platforms)

        if plat is not None:
            self.pm.jumped_platform_height = plat.height

            save_plat = self.pm.create_saving_platform()
            self.objects.append(save_plat)
            self.platforms.append(save_plat)

            if isinstance(plat, platform.FakePlatform):
                self.sounds.play_sound("fake_break")
                plat.move(0, c.win_height)
            else:
                # Jumper's jump event states
                self.collision_dist = abs(plat.top - self.jumper.bottom)
                self.jumper.isCollision = True

                self.sounds.play_sound("jump")
                plat.color = colors.RED1
                plat_was_jumped = 1

        height_dif = self.camera_chasing()

        # Background moving
        self.height_passed += height_dif
        if self.height_passed >= self.height_to_one_pixel_move:
            self.background.change_offset(0, 1)
            self.height_passed -= self.height_to_one_pixel_move

        self.update_points(height_dif, plat_was_jumped)

        if self.pm.tracking_platform.top >= 0:
            platforms = self.pm.another_platforms()
            for p in platforms:
                self.objects.append(p)
                self.platforms.append(p)

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
        create_scroller(self, self.buttons[0].right+50, self.buttons[0].top-25,
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
        create_scroller(self, self.buttons[1].right+50, self.buttons[1].top-25,
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
