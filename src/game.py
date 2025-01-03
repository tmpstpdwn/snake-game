#!/bin/python3

### IMPORTS ###

import pygame
import random
from settings import *
from snake import SnakeBlock
from food import FoodBlock
from os.path import join

### CLASSES ###

class Game:

    # Init necessary variables.
    def __init__(self):

        # SCREEN
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # FONT
        self.font = pygame.font.Font(join('..', 'fonts', 'pix.ttf'), 30)

        # SNAKE AND FOOD
        self.snake = [SnakeBlock((self.get_random_position()))]
        for i in range(3):
            self.add_block()
        self.head = self.snake[0]
        self.food = FoodBlock(self.get_random_position())

        # ADD MOVEMENT DELAY
        self.movement_delay = 80
        self.prev_movement = 0

        # SCORE & GAMEOVER
        self.score = 0
        self.game_over = False

        # CLOCK
        self.clock = pygame.time.Clock()
        self.is_running = True

    # Get random position on the grid.
    def get_random_position(self):
        x = random.randint(1, WIDTH//SIZE - SIZE//2)
        y = random.randint(1, HEIGHT//SIZE - SIZE//2)
        return x, y

    # Get events and manage.
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    # Get input.
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.head.direction.y == 0:
            self.head.direction.update(0, -1)
        elif keys[pygame.K_LEFT] and self.head.direction.x == 0:
            self.head.direction.update(-1, 0)
        elif keys[pygame.K_RIGHT] and self.head.direction.x == 0:
            self.head.direction.update(1,  0)
        elif keys[pygame.K_DOWN] and self.head.direction.y == 0:
            self.head.direction.update(0,  1)

    # Move the snake.
    def move(self):
        if pygame.time.get_ticks() - self.prev_movement > self.movement_delay:
            for i in range(len(self.snake) - 1, 0, -1):
                self.snake[i].direction.update(self.snake[i-1].direction) 
                self.snake[i].rect.center = self.snake[i-1].rect.center
            self.head.rect.center += self.head.direction * SIZE
            self.prev_movement = pygame.time.get_ticks()

    # Add snake block.
    def add_block(self):
        tail_direction = self.snake[-1].direction
        tail_centerx = self.snake[-1].rect.centerx
        tail_centery = self.snake[-1].rect.centery

        if tail_direction.x < 0:
            x, y = tail_centerx + SIZE, tail_centery
            self.snake.append(SnakeBlock((x, y)))
        elif tail_direction.x > 0:
            x, y = tail_centerx - SIZE, tail_centery
            self.snake.append(SnakeBlock((x, y)))
        elif tail_direction.y < 0:
            x, y = tail_centerx, tail_centery + SIZE
            self.snake.append(SnakeBlock((x, y)))
        elif tail_direction.x < 0:
            x, y = tail_centerx, tail_centery - SIZE
            self.snake.append(SnakeBlock((x, y)))

    # Add food block.
    def add_food(self):
        not_found = True
        while not_found:
            new_food_pos = self.get_random_position()
            new_food_rect = self.food.rect.copy()
            new_food_rect.center = (new_food_pos[0] * SIZE, new_food_pos[1] * SIZE)
            for block in self.snake:
                if new_food_rect.colliderect(block):
                    break
            else:
                not_found = False
                self.food.new_pos(new_food_pos)

    # Detect collition with food and grow the snake.
    def food_collision_and_growth(self):
        if self.head.rect.colliderect(self.food.rect):
            self.add_block()
            self.add_food()
            self.score += 1
            if self.movement_delay > 35:
                self.movement_delay -= 1

    # Detect collition with the body and restart the game.
    def collision_with_body(self):
        for block in self.snake[1:]:
            if self.head.rect.colliderect(block.rect):
                self.game_over = True

    # Detect collition with the borders and teleport.
    def collision_with_border(self):
        if self.head.rect.centerx > WIDTH:
            self.head.rect.centerx = 0 
        if self.head.rect.centerx < 0:
            self.head.rect.centerx = WIDTH
        if self.head.rect.centery > HEIGHT:
            self.head.rect.centery = 0
        if self.head.rect.centery < 0:
            self.head.rect.centery = HEIGHT

    # Detect collitions.
    def collision(self):
        self.food_collision_and_growth()
        self.collision_with_body()
        self.collision_with_border()

    # Score.
    def score_board(self):
        score_text = self.font.render(str(self.score), False, 'black')
        score_rect = score_text.get_frect(center = (WIDTH//2, HEIGHT - 50))
        self.screen.blit(score_text, score_rect)
        pygame.draw.rect(self.screen, 'black', score_rect.inflate(30, 20).move(0, -5), 2, 5)

    # Display "GAME OVER" when it does.
    def gameo(self):
        gameo_text = self.font.render("GAME OVER", False, 'red')
        gameo_rect = gameo_text.get_frect(center = (WIDTH/2, HEIGHT/2))
        self.screen.blit(gameo_text, gameo_rect)
        pygame.draw.rect(self.screen, 'black', gameo_rect.inflate(20, 20).move(0, -5), 2, 5)

    # Draw onto display surface.
    def draw(self):
        for block in self.snake:
            self.screen.blit(block.image, block.rect)
        self.screen.blit(self.food.image, self.food.rect)
        self.score_board()
        if self.game_over:
            self.gameo()
        pygame.display.update()

    # Fill screen with white.
    def fill(self):
        self.screen.fill('white')

    # Run the game.
    def run(self):
        while self.is_running:
            self.clock.tick()
            self.events()
            if not self.game_over:
                self.input()
                self.move()
                self.collision()
            self.fill()
            self.draw()

### END ###
