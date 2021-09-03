import pygame
import sys
from player import Player

class Game:
    def __init__(self):
        playerSprite = Player((screenWidth/2, screenHeight), screenWidth, 5)
        self.player = pygame.sprite.GroupSingle(playerSprite)

    def run(self):
        self.player.update()
        self.player.draw(screen)
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
