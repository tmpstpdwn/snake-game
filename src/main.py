### IMPORTS ###

import pygame
from game import Game
from helpers import install_missing_modules

### MAIN ###

install_missing_modules(["pygame-ce"])

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

### END ###
