import random


class RandomPlayer:
    def __init__(self, num):
        self.number = num

    def __str__(self):
        return "RandomPlayer"

    def choose(self, gameInst):
        return random.choice(gameInst.get_possible_moves())