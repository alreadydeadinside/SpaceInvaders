from aliens import Aliens


class Dummy(Aliens):
    def action(self, vel, player):
        self.y += vel
