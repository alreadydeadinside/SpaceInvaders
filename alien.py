import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y, game):
        super().__init__()
        file_path = 'sprites/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.kSpeed = 1
        self.game = game
        if color == 'red':
            self.value = 100
        elif color == 'green':
            self.value = 200
        else:
            self.value = 300

    def update(self, direction):
        self.rect.x += direction * self.kSpeed
        self.kSpeed = (self.game.score / 2000) + 1


class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screenWidth):
        super().__init__()
        self.image = pygame.image.load('sprites/extra.png').convert_alpha()

        if side == 'right':
            x = screenWidth + 50
            self.speed = - 3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        self.rect.x += self.speed
