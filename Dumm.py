from Invaders import Invaders


class Dummy(Invaders):
    def action(self, vel, player):
        self.y += vel
