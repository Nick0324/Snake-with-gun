import pygame
from pygame.locals import *
import time
import random

SIZE = 40


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 800))
        self.surface.fill((0, 255, 0))

        self.snake = Snake(self.surface)
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()

    def draw_objects(self):
        self.snake.move()
        self.apple.draw()

        if self.is_colliding(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()

            self.apple.move()

    def display_score(self):
        pygame.display.set_caption('Snake | Score: ' + str(self.snake.length - 1))

    def is_colliding(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.snake.set_direction("UP")
                    if event.key == K_DOWN:
                        self.snake.set_direction("DOWN")
                    if event.key == K_LEFT:
                        self.snake.set_direction("LEFT")
                    if event.key == K_RIGHT:
                        self.snake.set_direction("RIGHT")

            self.display_score()

            self.draw_objects()
            time.sleep(0.3)


class Snake:
    def __init__(self, screen):
        self.length = 1
        self.screen = screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * self.length
        self.y = [SIZE] * self.length
        self.facing_direction = "RIGHT"

    def draw(self):
        self.screen.fill((0, 255, 0))

        for i in range(self.length):
            self.screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.facing_direction == "UP":
            self.y[0] -= SIZE
            self.draw()
        if self.facing_direction == "DOWN":
            self.y[0] += SIZE
            self.draw()
        if self.facing_direction == "LEFT":
            self.x[0] -= SIZE
            self.draw()
        if self.facing_direction == "RIGHT":
            self.x[0] += SIZE
            self.draw()

    def set_direction(self, direction):
        if direction == "UP":
            self.facing_direction = "UP"
        if direction == "DOWN":
            self.facing_direction = "DOWN"
        if direction == "LEFT":
            self.facing_direction = "LEFT"
        if direction == "RIGHT":
            self.facing_direction = "RIGHT"


class Apple:
    def __init__(self, screen):
        self.sprite = pygame.image.load("resources/apple.jpg").convert()
        self.screen = screen
        self.x = 400
        self.y = 400

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x, self.y = random.randint(0, 20) * SIZE, random.randint(0, 20) * SIZE


if __name__ == '__main__':
    game = Game()
    game.run()