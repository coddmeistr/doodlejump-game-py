import pygame.image


class Background:
    def __init__(self, image):
        self.current_background = pygame.image.load(image)
        self.tag = "*export*"
        self.offset = (0, 0)

        self.menu_backgrounds = {"default": pygame.image.load("images/background.jpg")
                            }
        self.menu_background_offsets = {"default": (0, 0)
                                        }

        self.levels_backs = {"level_1": pygame.image.load("images/levels_backs/level_1_back.jpg")
                        }
        self.levels_backs_offsets = {"level_1": (0, -200)}

    def change_background_filename(self, image):
        self.current_background = pygame.image.load(image)

    def change_background_menu(self, tag):
        self.current_background = self.menu_backgrounds[tag]
        self.offset = self.menu_background_offsets[tag]
        self.tag = tag

    def change_background_game(self, tag):
        self.current_background = self.levels_backs[tag]
        self.offset = self.levels_backs_offsets[tag]
        self.tag = tag

    def next_level_back(self):
        if "level" in self.tag:
            new_tag = "level_"+str(int(self.tag[6])+1)
            self.current_background = self.levels_backs[new_tag]
            self.offset = self.levels_backs_offsets[new_tag]
            self.tag = new_tag

    def change_offset(self, dx, dy):
        self.offset = tuple([self.offset[0]+dx, self.offset[1]+dy])

    def set_offset(self, offset):
        self.offset = tuple([offset[0], offset[1]])

    def draw(self, surface):
        surface.blit(self.current_background, self.offset)

