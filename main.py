import random
from fileWrite import csv_write
from settings import *
from obstacles import Asteroid
from dummyAlien import *
from player import Player
from aliens import Aliens
from algorithm import *

pygame.font.init()

green = (0, 255, 0)
red = (255, 0, 0)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    global method
    playing = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.Font("assets/Pixeled.ttf", 20)
    lost_font = pygame.font.Font("assets/Pixeled.ttf", 20)

    invaders = []
    bunkers = []
    wave_length = 1
    enemy_vel = 1

    player_vel = 20
    laser_vel = 30

    player = Player(330, 630)
    for i in range(4):
        bunkers.extend(
            [Asteroid(random.randrange(0, 750), random.randrange(0, 750 - YELLOW_SPACE_SHIP.get_height() - 50))])

    clock = pygame.time.Clock()

    cast_away = False  # lost
    lost_count = 0

    def invadersHold():
        lasers = []
        for i in invaders:
            for laser in i.lasers:
                lasers.append(laser)
        return lasers

    def drawWindow():
        WIN.blit(BG, (0, 0))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        player.shoot()
        for invader in invaders:
            invader.draw(WIN)

        player.draw(WIN)

        if cast_away:
            lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 22, 350))
    while playing:
        clock.tick(FPS)
        if lives <= 0 or player.health <= 0:
            cast_away = True
            lost_count += 1

        if cast_away:
            if lost_count > FPS * 6:
                playing = False
            else:
                continue

        if len(invaders) == 0:
            level += 1
            wave_length += 2
            for i in range(wave_length):
                invaders.append(Dummy(random.randrange(50, WIDTH - 100), random.randrange(10, 200),
                                      random.choice(["red", "blue", "green"])))
                invaders.append(Aliens(random.randrange(50, WIDTH - 100), random.randrange(10, 200),
                                       random.choice(["red", "blue", "green"])))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    method = snext(method)
                    print(method)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for bunker in bunkers:
            if collide(player, bunker):
                bunkers.remove(bunker)
                print(1)
            elif bunker.y + bunker.get_height() > HEIGHT:
                lives -= 1
                bunkers.remove(bunker)

        import time
        start_time = time.time()
        (alpha_beta_result, direction) = alphabeta(Node(player, invaders, invadersHold(), '', bunkers), depth_recursion,
                                                   -float('inf'), float('inf'), False)
        print((alpha_beta_result, direction.move))
        dirs = {"<": (-8, 0), ">": (8, 0), '': (0, 0)}
        player.x += dirs[direction.move][0]
        lasers = []
        for i in invaders:
            for laser in i.lasers:
                lasers.append(laser)
        for bul in lasers:
            if bul.x in range(int(player.x) - int(RED_LASER.get_width()), int(player.x) + int(
                    YELLOW_SPACE_SHIP.get_width())) and bul.y < player.y + YELLOW_SPACE_SHIP.get_height() and player.y - (
                    bul.y + RED_LASER.get_height()) < 100:
                if player.x + YELLOW_SPACE_SHIP.get_width() / 2 - bul.x + RED_LASER.get_width() / 2 < 0:
                    if player.x - abs(player_vel) > 0:
                        player.x -= abs(player_vel + 10)
                    else:
                        player.x += abs(player_vel + 10)
                elif player.x + YELLOW_SPACE_SHIP.get_width() / 2 - bul.x + RED_LASER.get_width() / 2 > 0:
                    if player.x + YELLOW_SPACE_SHIP.get_width() + abs(player_vel) < WIDTH:
                        player.x += abs(player_vel + 10)
                    else:
                        player.x -= abs(player_vel + 10)

        for bunker in bunkers:
            bunker.draw(WIN)
        for invader in invaders[:]:
            invader.action(enemy_vel, player)
            invader.move_lasers(laser_vel, player, bunkers)

            if random.randrange(0, 2 * 60) == 1:
                invader.shoot()

            if collide(invader, player):
                player.health -= 10
                invaders.remove(invader)
            elif invader.y + invader.get_height() > HEIGHT:
                lives -= 1
                invaders.remove(invader)

        player.move_lasers(-laser_vel, invaders, bunkers)

        csv_write('output.csv',
                  [str(cast_away), str(time.time() - start_time), str(level), 'alpha-beta pruning', 'expectimax minimax'])

        pygame.display.update()
        drawWindow()


def main_menu():
    playing = True
    main()
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
    pygame.quit()


main_menu()
