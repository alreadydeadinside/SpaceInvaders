import pygame as pg
import math


class Game:
    pg.init()
    fonts = pg.font.Font('font/Pixeled.ttf', 20)
    score = 0
    aliens_count = 0

    def updateScore(self, score_pos_x, score_pos_y, screen):
        main_score = self.fonts.render("SCORE: " + str(self.score), True, (255, 255, 255))
        screen.blit(main_score, (score_pos_x, score_pos_y))

    def createCollision(self, aliens_w, aliens_h, bullet_w, bullet_h):
        collision = math.sqrt((math.pow(aliens_w - bullet_w, 2)) + (math.pow(aliens_h - bullet_h, 2)))
        if collision < 30:
            return True
        else:
            return False

    def asteroidCollision(self, aster_w, aster_h, bullet_w, bullet_h):
        isCollision = math.sqrt((math.pow(aster_w - bullet_w, 2)) + (math.pow(aster_h - bullet_h, 2)))
        if isCollision < 55:
            return True
        else:
            return False

    def setScore(self, temp):
        self.score += temp

    def asteroidsCoordinates(self, asteroids):
        asteroid_pos = []
        for i in range(asteroids.asteroids_counter):
            asteroid_pos.append(asteroids.asteroidsPosition(i))

        return asteroid_pos

    def winMessage(self, screen):
        gameOverTitle = self.fonts.render("You win!", True, (255, 255, 255))
        screen.blit(gameOverTitle, (250, 250))

    def loseMessage(self, screen):
        gameOverTitle = self.fonts.render("You lose!", True, (255, 255, 255))
        screen.blit(gameOverTitle, (250, 250))
