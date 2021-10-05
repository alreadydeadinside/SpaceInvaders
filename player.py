import pygame as pg


class Player:
    player_asset = pg.image.load('pict/player.png')
    bullet_asset = pg.image.load('pict/bullet.png')
    player_position_x = 400
    player_position_y = 500
    player_speed = 0
    bullet_position_x = 350
    bullet_position_y = 500
    bullet_speed = 2
    bullet_state = "ready"

    def drawPlayer(self, player_w, player_h, screen):
        screen.blit(self.player_asset, (player_w, player_h))

    def playerSpeed(self, temp):
        self.player_speed = temp

    def getPlayerWidth(self):
        return self.player_position_x

    def getPlayerPos(self):
        widthPlace = int(self.player_position_x / 64)
        heightPlace = int(self.player_position_y / 64)
        return heightPlace, widthPlace

    def boundsLines(self):
        if self.player_position_x <= 0:
            self.player_position_x = 0
        elif self.player_position_x >= 740:
            self.player_position_x = 740

    def bullet(self, bullet_w, bullet_h, screen):
        self.bullet_state = "not ready"
        screen.blit(self.bullet_asset, (bullet_w + 16, bullet_h + 10))

    def bulletWidth(self, coord):
        self.bullet_position_x = coord

    def bulletHeight(self):
        return self.bullet_position_x

    def bulletState(self, temp):
        self.bullet_state = temp

    def bulletSpeed(self):
        self.bullet_position_y -= self.bullet_speed

    def setBulletHeight(self, change):
        self.bullet_position_y = change

    def changeYPosition(self, change):
        self.bullet_position_y += change

    def getBulletSpeed(self):
        return self.bullet_speed

    def setPlayerWidth(self, x):
        self.player_position_x += x

    def getPlayerSpeed(self):
        return self.player_speed

    def getPlayerH(self):
        return self.player_position_y

    def getBulletState(self):
        return self.bullet_state

    def getBulletHeight(self):
        return self.bullet_position_y
