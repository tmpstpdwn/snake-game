### IMPORTS ###

import pygame
from settings import *

### CLASSES ###

class SnakeBlock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((SIZE, SIZE))
        self.image.fill('green')
        self.rect = self.image.get_frect(center = (pos[0]*SIZE, pos[1]*SIZE))
        self.direction = pygame.math.Vector2(1, 0)

### END ###
