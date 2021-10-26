from settings import *
from ship import Ship


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.win = False
        self.score = 0
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, *args):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for objs in args:
                    for obj in objs:
                        if laser.collision(obj):
                            objs.remove(obj)
                            if laser in self.lasers:
                                self.lasers.remove(laser)

    def copy_object(self):
        res = Player(self.x, self.y, self.health)
        res.lasers = [laser.copy_object() for laser in self.lasers]
        return res

    def draw(self, window):
        super().draw(window)
