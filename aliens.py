import pygame as pg
import random


class Aliens:
    aliens_count = 5
    number_aliens_for_alg = 5
    aliens_x_position_on_path = []
    aliens_y_position_on_path = []
    aliens_pics = []
    aliens_change_spees = []
    aliens_position_y_change_on_path = []
    asteroids_pics = []
    asteroid_position_x = []
    asteroid_position_y = []
    asteroid_health = []
    asteroids_counter = 4

    def generateAliens(self):
        for i in range(self.aliens_count):
            self.aliens_pics.append(pg.image.load('pict/aliens.png'))
            self.aliens_x_position_on_path.append(random.randint(0, 700))
            self.aliens_y_position_on_path.append(random.randint(50, 150))

            self.aliens_change_spees.append(0.2)
            self.aliens_position_y_change_on_path.append(50)

    def aliens(self, alien_w, alien_h, i, screen):
        screen.blit(self.aliens_pics[i], (alien_w, alien_h))

    def getAliensPosition(self, i):
        if self.aliens_x_position_on_path[i] <= 800 and self.aliens_y_position_on_path[i] <= 512:
            x_coordinate = int(self.aliens_x_position_on_path[i] / 64)
            y_coordinate = int(self.aliens_y_position_on_path[i] / 64)
        else:
            x_coordinate = -1
            y_coordinate = -1
        return y_coordinate, x_coordinate

    def asteroidsHealth(self, bullet, game, screen, aliens):
        for i in range(self.asteroids_counter):

            self.drawAsteroids(screen, i, self.asteroid_position_x[i], self.asteroid_position_y[i])

            collision = game.asteroidCollision(self.asteroid_position_x[i], self.asteroid_position_y[i],
                                               bullet.bulletHeight(),
                                               bullet.getBulletHeight())
            if collision:
                bullet.setBulletHeight(470)
                bullet.bulletState("ready")
                self.asteroid_health[i] -= 1

            if self.asteroid_health[i] == 0:
                self.asteroid_position_y[i] = 2700
            self.drawAsteroids(screen, i, self.asteroid_position_x[i], self.asteroid_position_y[i])
            if aliens.getAliensCount() == 0:
                for i in range(self.asteroids_counter):
                    self.asteroid_position_y[i] = 2700

    def aliensMove(self, game, bullet, screen, asteroids):

        for i in range(self.aliens_count):
            self.aliens_x_position_on_path[i] += self.aliens_change_spees[i]
            if self.aliens_x_position_on_path[i] <= 0:
                self.aliens_change_spees[i] = 0.5
                self.aliens_y_position_on_path[i] += self.aliens_position_y_change_on_path[i]
            elif self.aliens_x_position_on_path[i] >= 740:
                self.aliens_change_spees[i] = -0.5
                self.aliens_y_position_on_path[i] += self.aliens_position_y_change_on_path[i]
            self.aliens(self.aliens_x_position_on_path[i], self.aliens_y_position_on_path[i], i, screen)

            collision = game.createCollision(self.aliens_x_position_on_path[i], self.aliens_y_position_on_path[i],
                                             bullet.bulletHeight(),
                                             bullet.getBulletHeight())
            if collision:
                bullet.setBulletHeight(470)
                bullet.bulletState("ready")
                game.setScore(100)
                self.aliens_y_position_on_path[i] = 3000
            self.aliens(self.aliens_x_position_on_path[i], self.aliens_y_position_on_path[i], i, screen)
            if game.score == 500:
                for i in range(asteroids.asteroids_counter):
                    asteroids.asteroid_position_x[i] = 1500
                game.winMessage(screen)
                break
            if 500 <= self.aliens_y_position_on_path[i] <= 600:
                for j in range(self.aliens_count):
                    self.aliens_y_position_on_path[j] = 1500
                    self.aliens_change_spees[i] = 0
                for i in range(asteroids.asteroids_counter):
                    asteroids.asteroid_position_y[i] = 1500
                game.loseMessage(screen)
                break

    def getAliensCount(self):
        return self.aliens_count

    def drawAsteroids(self, screen, i, aster_coordinate_x, asteroid_coordinate_y):
        screen.blit(self.asteroids_pics[i], (aster_coordinate_x, asteroid_coordinate_y))

    def asteroidsPosition(self, i):
        if self.asteroid_position_x[i] <= 800 and self.asteroid_position_y[i] <= 512:
            position_x = int(self.asteroid_position_x[i] / 64)
            position_y = int(self.asteroid_position_y[i] / 64)
        else:
            position_x = 0
            position_y = 8
        return position_y, position_x

    def generateAsteroids(self):
        temp = 1
        for i in range(self.asteroids_counter):
            if temp == 1:
                self.asteroid_position_x.append(60)
                self.asteroid_position_y.append(360)
            if temp == 2:
                self.asteroid_position_x.append(340)
                self.asteroid_position_y.append(360)
            if temp == 3:
                self.asteroid_position_x.append(650)
                self.asteroid_position_y.append(360)
            if temp == 4:
                self.asteroid_position_x.append(180)
                self.asteroid_position_y.append(250)
            self.asteroids_pics.append(pg.image.load('pict/asteroid.png'))
            self.asteroid_health.append(2)
            temp += 1


