from MODULES import *


class Music:
    def __init__(self, volume):
        # Music themes dict
        self.music_themes = dict()
        self.volume = volume
        pygame.mixer_music.set_volume(self.volume)
        # Add music themes here
        self.music_themes["menu"] = "music/background_lane.mp3"
        self.music_themes["play"] = "music/background_steins_gate.mp3"

    def set_music_theme(self, tag):
        pygame.mixer.music.load(self.music_themes[tag])
        pygame.mixer.music.play(-1)

    def change_volume(self, new):
        pygame.mixer_music.set_volume(new)
        self.volume = new
