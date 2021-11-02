import pygame.mixer

from MODULES import *


class Music:
    def __init__(self, volume):
        # Music themes dict
        self.music_themes = dict()
        self.volume = volume
        pygame.mixer_music.set_volume(self.volume/100)
        # Add music themes here
        self.music_themes["menu"] = "music/background_lane.mp3"
        self.music_themes["play"] = "music/background_steins_gate.mp3"

    def set_music_theme(self, tag):
        pygame.mixer.music.load(self.music_themes[tag])
        pygame.mixer.music.play(-1)

    def change_volume(self, new):
        pygame.mixer_music.set_volume(new)
        self.volume = new


class Sounds:
    def __init__(self, volume):
        # Sounds dict
        self.sounds = dict()
        self.volume = volume
        # Add sounds here
        self.sounds["jump"] = pygame.mixer.Sound("sounds/jump.wav")
        for sound in self.sounds.items():
            pygame.mixer.Sound.set_volume(sound[1], self.volume/100)

    def play_sound(self, tag):
        self.sounds[tag].play()

    def change_volume(self, new):
        for sound in self.sounds.items():
            pygame.mixer.Sound.set_volume(sound[1], new)
        self.volume = new
