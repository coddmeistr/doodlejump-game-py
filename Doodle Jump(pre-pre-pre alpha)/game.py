import pygame.mixer_music
from MODULES import *
from music_sounds import *
import multicoloring
from collections import defaultdict


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
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
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
        self.volume_music = 0
        self.volume_sounds = 0
        self.difficulty = 0
        self.load_settings()

        self.music = Music(self.volume_music)

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
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def load_settings(self):
        file_music = open("settings/music.txt")
        file_sounds = open("settings/sounds.txt")
        self.volume_music = float(file_music.readline())
        self.volume_sounds = float(file_sounds.readline())
        file_music.close()
        file_sounds.close()

    def save_settings(self):
        file_music = open("settings/music.txt")
        file_sounds = open("settings/sounds.txt")
        file_music.write(str(self.volume_music))
        file_sounds.write(str(self.volume_sounds))
        file_music.close()
        file_sounds.close()

    def run(self):
        while not self.game_ending:
            self.surface.blit(self.background_image_menu, (0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
