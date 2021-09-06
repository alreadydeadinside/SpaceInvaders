from random import choice, randint
from laser import Laser
from alien import Alien, Extra
import pygame
import sys
from player import Player
import obstacle


class Game:
    def __init__(self):
        # player setup
        playerSprite = Player((screenWidth / 2, screenHeight), screenWidth, 5)
        self.player = pygame.sprite.GroupSingle(playerSprite)

        # obstacle setup
        self.shape = obstacle.shape
        self.block_size = 5
        self.blocks = pygame.sprite.Group()
        self.obstacles_amount = 8
        self.obstacles_x_position = [
            num * (screenWidth / self.obstacles_amount) for num in range(self.obstacles_amount)]
        self.generateMultipleObstacles(
            *self.obstacles_x_position, x_start=screenWidth / 30, y_start=680)

        # aliens setup + extra
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alienSetup(rows=6, cols=8)
        self.alien_direction = 1

        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

        # health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('player.png').convert_alpha()
        self.live_x_start_pos = screenWidth - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font("Pixeled.ttf", 20)

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
                    alienSprite = Alien('yellow', x, y, self)
                elif 1 <= row_index <= 2:
                    alienSprite = Alien('green', x, y, self)
                else:
                    alienSprite = Alien('red', x, y, self)
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

    def alienShoot(self):
        if self.aliens.sprites():
            randomAlien = choice(self.aliens.sprites())
            laserSprite = Laser(randomAlien.rect.center, 6, screenHeight)
            self.alien_lasers.add(laserSprite)

    def extraAlienTimer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screenWidth))
            self.extra_spawn_time = randint(400, 800)

    def collisionChecks(self):

        # player lasers 
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()

                # extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()

        # alien lasers 
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()


        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def displayLives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def displayScore(self):
        scoreSurf = self.font.render(f'score: {self.score}', False, 'white')
        scoreRect = scoreSurf.get_rect(topleft=(10, -10))
        screen.blit(scoreSurf, scoreRect)

    def victoryMessage(self):
        if not self.aliens.sprites():
            victorySurf = self.font.render('You won', False, 'white')
            victoryRect = victorySurf.get_rect(center=(screenWidth / 2, screenHeight / 2))
            screen.blit(victorySurf, victoryRect)

    def run(self):
        self.player.update()
        self.player.draw(screen)
        self.player.sprite.lasers.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.aliens.update(self.alien_direction)
        self.alienPositionChecker()
        self.alien_lasers.update()
        self.extra.update()
        self.extraAlienTimer()
        self.collisionChecks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.displayLives()
        self.displayScore()
        self.victoryMessage()

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
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 500)

    while True:
        keys = pygame.key.get_repeat()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alienShoot()
        screen.fill((30, 30, 30))
        game.run()
        pygame.display.flip()
        fps.tick(60)
