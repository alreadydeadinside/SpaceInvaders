from player import Player
from aliens import Aliens
import pygame as pg
from graph import generatePath
from graph import map_graph
from game import Game

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Space Invaders")
icon = pg.image.load('pict/space-invaders.png')
pg.display.set_icon(icon)
background_picture = pg.image.load('pict/space-bg.jpg')
player = Player()
aliens = Aliens()
bullet = Player()
game = Game()
asteroids = Aliens()
aliens.generateAliens()
bfs, dfs, ucs = 0, 0, 0
asteroids.generateAsteroids()
close = True

while close:
    screen.fill((0, 0, 0))
    screen.blit(background_picture, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            close = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                player.playerSpeed(1.5)
            if event.key == pg.K_LEFT:
                player.playerSpeed(-1.5)
            if event.key == pg.K_SPACE:
                if bullet.getBulletState() == "ready":
                    bullet.bulletWidth(player.getPlayerWidth())
                    bullet.bullet(bullet.bulletHeight(), bullet.getBulletHeight(), screen)
                    bullet.changeYPosition(-bullet.getBulletSpeed())
            if event.key == pg.K_z:
                print('BFS:')
                bfs, dfs, ucs = 1, 0, 0
            if event.key == pg.K_a:
                print('UCS:')
                bfs, dfs, ucs = 0, 0, 1
            if event.key == pg.K_q:
                print('DFS:')
                bfs, dfs, ucs = 0, 1, 0
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                player.playerSpeed(0)

    player.setPlayerWidth(player.getPlayerSpeed())
    if bullet.getBulletHeight() <= 0:
        bullet.bulletState("ready")
        bullet.setBulletHeight(470)
    aliens.aliensMove(game, bullet, screen, asteroids)
    asteroids.asteroidsHealth(bullet, game, screen, aliens)
    if bullet.getBulletState() == "not ready":
        bullet.bullet(bullet.bulletHeight(), bullet.getBulletHeight(), screen)
        bullet.changeYPosition(-bullet.getBulletSpeed())
    player.boundsLines()
    if aliens.getAliensCount() == 0:
        game.winMessage(screen)
        temp = False
    asteroid_coordinates = game.asteroidsCoordinates(asteroids)
    if bfs == 1:
        generatePath(screen, aliens, map_graph, player, asteroid_coordinates, 2)
    if dfs == 1:
        generatePath(screen, aliens, map_graph, player, asteroid_coordinates, 3)
    if ucs == 1:
        generatePath(screen, aliens, map_graph, player, asteroid_coordinates, 1)
    player.drawPlayer(player.getPlayerWidth(), player.getPlayerH(), screen)
    game.updateScore(15, 10, screen)
    pg.display.update()
