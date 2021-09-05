from laser import Laser
from pygame import time
from alien import Alien
import pygame
import sys
from player import Player
import obstacle
import time


class Game:
    def __init__(self):
        # player setup
        playerSprite = Player((screenWidth/2, screenHeight), screenWidth, 5)
        self.player = pygame.sprite.GroupSingle(playerSprite)

        # obstacle setup
        self.shape = obstacle.shape
        self.block_size = 5
        self.blocks = pygame.sprite.Group()
        self.obstacles_amount = 8
        self.obstacles_x_position = [
            num * (screenWidth / self.obstacles_amount) for num in range(self.obstacles_amount)]
        self.generateMultipleObstacles(
            *self.obstacles_x_position, x_start=screenWidth/30, y_start=680)

        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alienSetup(rows=6, cols=8)
        self.alien_direction = 1

   # ===== Obstacle Methods =====
    def generateObstacle(self, x_start, y_start, offset_x):
        # enumarate is to know, on what row we are
        for rowIndex, row in enumerate(self.shape):
            for colIndex, col in enumerate(row):
                if col == 'x':
                    x = x_start + colIndex * self.block_size + offset_x
                    y = y_start + rowIndex * self.block_size
                    block = obstacle.Block(self.block_size, 'green', x, y)
                    self.blocks.add(block)

    def generateMultipleObstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.generateObstacle(x_start, y_start, offset_x)

    # ==== Aliens methods ====
    def alienSetup(self, rows, cols, x_distance=90, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    alienSprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alienSprite = Alien('green', x, y)
                else:
                    alienSprite = Alien('red', x, y)
                self.aliens.add(alienSprite)

    def alienPositionChecker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screenWidth:
                self.alien_direction = -1
                self.alienMoveDown(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alienMoveDown(2)

    def alienMoveDown(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screenHeight)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def run(self):
        self.player.update()
        self.player.draw(screen)
        self.player.sprite.lasers.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.aliens.update(self.alien_direction)
        self.alienPositionChecker()
        # update all sprite groups
        # draw all sprite groups


if __name__ == "__main__":
    pygame.init()  # game start
    screenWidth = 800
    screenHeight = 800
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    fps = pygame.time.Clock()
    gameIcon = pygame.image.load("space_invaders_1.png")
    pygame.display.set_icon(gameIcon)
    pygame.display.set_caption("Space Invaders")
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))
        game.run()
        pygame.display.flip()
        fps.tick(60)
