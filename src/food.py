### IMPORTS ###

import pygame
from settings import *

### CLASSES ###

class FoodBlock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill('red')
        self.rect = self.image.get_frect(center = (pos[0]*SIZE, pos[1]*SIZE))

    def new_pos(self, pos):
        self.rect = self.image.get_frect(center = (pos[0]*SIZE, pos[1]*SIZE))

### END ###
