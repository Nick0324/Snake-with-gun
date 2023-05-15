import random
import time

import pygame
from pygame.locals import *

SIZE = 40


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 800))
        self.backgroundX = 0
        self.draw_background()

        self.snake = Snake(self.surface)
        self.snake.draw()

        #generate which fruit to spawn
        self.fruitID = 0
        self.apple = Apple(self.surface)
        self.generate_fruit()
        self.apple.draw()

    def generate_fruit(self):
        self.fruitID = random.randint(0, 2)
        match self.fruitID:
            case 0:
                self.apple = Apple(self.surface)
            case 1:
                self.apple = Coconut(self.surface)
            case 2:
                self.apple = Pepper(self.surface)

    def draw_objects(self):
        self.draw_background()
        self.snake.move()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # colliding with apple
        if self.is_colliding(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.generate_fruit()
            self.apple.move()

        # colliding with segment
        for i in range(3, self.snake.length):
            if self.is_colliding(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game over!"

        # draw the apple in a position different to the snake
        # for i in range(0, self.snake.length):
        # while self.snake.x[i] == self.apple.x and self.snake.y[i] == self.apple.y:
        # self.apple.move()

    def display_score(self):
        pygame.display.set_caption('Snake | Score: ' + str(self.snake.length - 1))

    def show_game_over(self):
        self.draw_background()
        Font = pygame.font.SysFont('arial', 30)
        line1 = Font.render(f"Game is over! Your score is {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = Font.render(f"Press enter to play again. Press escape to exit.", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface)
        self.snake.length = 1
        self.apple = Apple(self.surface)

    def draw_background(self):
        bg1 = pygame.image.load("resources/background.jpg").convert()
        bg2 = pygame.image.load("resources/background.jpg").convert()
        self.surface.blit(bg1, (self.backgroundX, 0))
        self.surface.blit(bg2, (self.backgroundX - 800, 0))
        self.backgroundX += 3
        if self.backgroundX == 800:
            self.backgroundX = 0

    def is_colliding(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        pause = False
                    if event.key == K_ESCAPE:
                        running = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.set_direction("UP")
                        if event.key == K_DOWN:
                            self.snake.set_direction("DOWN")
                        if event.key == K_LEFT:
                            self.snake.set_direction("LEFT")
                        if event.key == K_RIGHT:
                            self.snake.set_direction("RIGHT")

            try:
                if not pause:
                    self.draw_objects()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
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
        for i in range(self.length):
            self.screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def check_out_of_bounds(self):
        if self.x[0] < 0:
            self.x[0] = 800
        if self.x[0] > 800:
            self.x[0] = 0
        if self.y[0] < 0:
            self.y[0] = 800
        if self.y[0] > 800:
            self.y[0] = 0

    def move(self):
        self.check_out_of_bounds()

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
            if self.facing_direction != "DOWN" or self.length == 1:
                self.facing_direction = "UP"
        if direction == "DOWN":
            if self.facing_direction != "UP" or self.length == 1:
                self.facing_direction = "DOWN"
        if direction == "LEFT":
            if self.facing_direction != "RIGHT" or self.length == 1:
                self.facing_direction = "LEFT"
        if direction == "RIGHT":
            if self.facing_direction != "LEFT" or self.length == 1:
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
        self.x, self.y = random.randint(0, 19) * SIZE, random.randint(0, 19) * SIZE


class Coconut(Apple):

    hasShell = True

    def __init__(self, screen):
        self.sprite = pygame.image.load("resources/coconut.jpg").convert()
        self.screen = screen
        self.x = 400
        self.y = 400

    def remove_shell(self):
        self.sprite = pygame.image.load("resources/coconut_broken.jpg").convert()
        self.hasShell = False

class Pepper(Apple):
    def __init__(self, screen):
        self.sprite = pygame.image.load("resources/pepper.jpg").convert()
        self.screen = screen
        self.x = 400
        self.y = 400
        self.direction = random.randint(0, 3)
        self.projectile = pygame.image.load("resources/pepper_projectile.jpg").convert()
        self.projectilex = self.x
        self.projectiley = self.y

    def draw(self):
        match self.direction:
            case 0:
                self.projectiley -= SIZE
            case 1:
                self.projectilex += SIZE
            case 2:
                self.projectiley += SIZE
            case 3:
                self.projectilex -= SIZE
        if self.projectilex > 800 or self.projectilex < 0 or self.projectiley > 800 or self.projectiley < 0:
            match self.direction:
                case 0:
                    self.projectiley = self.y - SIZE
                case 1:
                    self.projectilex = self.x + SIZE
                case 2:
                    self.projectiley = self.y + SIZE
                case 3:
                    self.projectiley = self.y + SIZE
        self.screen.blit(self.sprite, (self.x, self.y))
        self.screen.blit(self.projectile, (self.projectilex, self.projectiley))
        pygame.display.flip()

    def move(self):
        self.x, self.y = random.randint(0, 19) * SIZE, random.randint(0, 19) * SIZE
        self.projectilex = self.x
        self.projectiley = self.y

if __name__ == '__main__':
    game = Game()
    game.run()
