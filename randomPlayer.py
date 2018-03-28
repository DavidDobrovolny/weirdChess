import random


class RandomPlayer:
    def __init__(self, num):
        self.number = num

    def choose(self, gameInst):
        return random.choice(gameInst.get_possible_moves())