import pygame.mixer_music
from music_sounds import *
from background import *
import multicoloring
from collections import defaultdict
from platform_manager import *
from movie import *
from pygame import cursors


class Game:
    def __init__(self,
                 caption,
                 width,
                 height,
                 back_image_filename,
                 frame_rate):
        self.background_image_menu = \
            pygame.image.load(back_image_filename)
        self.frame_rate = frame_rate
        self.game_ending = False
        self.objects = []
        self.objects_to_remove = []  # garbage collector with delayed remove
        self.platforms = []
        self.buttons = []
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.font.init()
        self.background = Background(back_image_filename)
        self.pm = PlatformManager(self)
        self.font = pygame.font.Font(c.font_name, c.font_size)
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

        # functionality
        self.multicolor = multicoloring.Multicolor()
        # errors
        self.errors_log = dict()
        self.errors_log[AttributeError] = ""
        self.errors_log[ValueError] = ""
        # settings
        self.music = Music()
        self.sounds = Sounds()
        self.load_settings()

        self.movie = Movie(self.music)
        self.anims = AnimationBase()

        pygame.mouse.set_visible(False)
        self.cursor_texture = pygame.image.load("textures/cursor/cursor.png")
        self.is_hide_cursor = False

    def update(self):
        pass

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_settings()
                # print(self.errors_log) # not necessary now
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def load_settings(self):
        file_music = open("settings/music.txt")
        file_sounds = open("settings/sounds.txt")
        self.music.change_volume(float(file_music.readline()))
        self.sounds.change_volume(float(file_sounds.readline()))
        file_music.close()
        file_sounds.close()

    def save_settings(self):
        file_music = open("settings/music.txt", "w")
        file_sounds = open("settings/sounds.txt", "w")
        file_music.write(str(self.music.volume))
        file_sounds.write(str(self.sounds.volume))
        file_music.close()
        file_sounds.close()

    def hide_cursor(self):
        self.is_hide_cursor = True

    def show_cursor(self):
        self.is_hide_cursor = False

    def run(self):
        while not self.game_ending:
            self.background.draw(self.surface)

            self.handle_events()
            self.update()
            self.draw()

            self.anims.update()
            self.movie.draw(self.surface)

            if not self.is_hide_cursor:
                cursor_rect = pygame.mouse.get_pos()  # update position
                cursor_rect = tuple([cursor_rect[0]-14, cursor_rect[1]])
                self.surface.blit(self.cursor_texture, cursor_rect)

            pygame.display.update()
            self.clock.tick(self.frame_rate)
