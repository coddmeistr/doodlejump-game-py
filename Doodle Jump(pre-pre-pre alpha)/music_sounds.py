import pygame.mixer

from MODULES import *


class Music:
    def __init__(self):
        self.tag = ""
        # Music themes dict
        self.music_themes = dict()
        self.volume = 0
        pygame.mixer_music.set_volume(self.volume)
        # Add music themes here
        self.music_themes["menu"] = "music/background_lane.mp3"
        self.music_themes["play"] = "music/background_steins_gate.mp3"
        self.music_themes["steins_gate_audio"] = "movies/reading_steiner_audio/reading_steiner_audio.mp3"

    def set_music_theme(self, tag, param=-1):
        self.tag = tag
        pygame.mixer.music.load(self.music_themes[tag])
        pygame.mixer.music.play(param)

    def change_volume(self, new):
        pygame.mixer_music.set_volume(new)
        self.volume = new


class Sounds:
    def __init__(self):
        # Sounds dict
        self.sounds = dict()
        self.volume = 0
        # Add sounds here
        self.sounds["jump"] = pygame.mixer.Sound("sounds/jump.wav")
        self.sounds["fake_break"] = pygame.mixer.Sound("sounds/fake_platform_break.wav")
        for sound in self.sounds.items():
            pygame.mixer.Sound.set_volume(sound[1], self.volume)

    def play_sound(self, tag):
        self.sounds[tag].play()

    def change_volume(self, new):
        for sound in self.sounds.items():
            pygame.mixer.Sound.set_volume(sound[1], new)
        self.volume = new
