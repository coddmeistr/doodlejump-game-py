import pygame
import os
import config as c


class Movie:
    def __init__(self, music_manager, base):
        self.base = base

        self.music_manager = music_manager

        self.current_frame = 0
        self.movie_frames_count = 0
        self.current_movie = []
        self.movie_size = (0, 0)

        self.prev_music_tag = ""

        self.movies = {"steins_gate": self.load_movie("movies/reading_steiner_frames")
                       }
        self.movie_sizes = {"steins_gate": c.s_steins_gate_movie}

        self.FPS = 60
        self.ticks_passed = 0
        self.skip_ticks = int(1 / (self.FPS / c.framerate)) - 1
        self.play_movie = False

    @staticmethod
    def load_movie(storage):
        movie = []
        for subdir, dirs, files in os.walk(storage):
            for file in files:
                movie.append(pygame.image.load(os.path.join(subdir, file)))
        return movie

    def start_movie(self, tag):
        self.prev_music_tag = self.music_manager.tag

        self.current_frame = 0
        self.current_movie = self.movies[tag]
        self.movie_frames_count = len(self.current_movie)
        self.play_movie = True
        self.movie_size = self.movie_sizes[tag]
        self.music_manager.set_music_theme(tag+"_audio", 1)

    def draw(self, surface):
        if self.play_movie:
            image = self.current_movie[self.current_frame].copy()
            image = pygame.transform.scale(image, self.base.resolution.get_scale(self.movie_size))
            surface.blit(image, (0, 0))

            if self.ticks_passed == self.skip_ticks:
                self.current_frame += 1
                self.ticks_passed = 0
            else:
                self.ticks_passed += 1

            if self.current_frame == self.movie_frames_count:
                self.play_movie = False
                self.music_manager.set_music_theme(self.prev_music_tag, -1)
