import pygame
import os

WIDTH, HEIGHT = 800, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Aliens")
accur = 50
size_of_enemies = 70
depth_recursion = 4
enemy_vel = 1
laser_vel = 30
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "red_alien.png"))
GREEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "green_alien.png")),(size_of_enemies, 50))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "yellow_alien.png"))
YELLOW_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "player.png")),(50 ,40))
BUNKER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "asteroid.png")),(90 ,90))
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.jpg")), (WIDTH, HEIGHT))

ENEMIES_HEURISTIC_CONSTANT = 20
MAX_ALFA_BETTA_RECURSION = 18


def snext(method):
    if method == 'star':
        return 'dfs'
    elif method == 'dfs':
        return 'bfs'
    elif method == 'bfs':
        return 'ucs'
    elif method == 'ucs':
        return 'star'


method = 'star'
