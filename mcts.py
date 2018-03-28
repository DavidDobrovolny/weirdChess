import random
import time
import copy


class MCTS:
    def __init__(self, num, t):
        self.number = num
        self.thinkTime = t

    def choose(self, gameInst):
        startTime = time.time()

        gameCopy = copy.deepcopy(gameInst)

        possible = {move : 0 for move in gameInst.get_possible_moves()}

        numGames = 0

        while time.time() - startTime < self.thinkTime:
            numGames += 1
            firstChoice = random.choice(list(possible.keys()))

            gameCopy.make_move(firstChoice)
            gameCopy.check_win()
            gameCopy.currentPlayer = 3 - gameCopy.currentPlayer

            i = 1

            while gameCopy.state == -1:
                choice = random.choice(gameCopy.get_possible_moves())
                i += 1

                gameCopy.make_move(choice)
                gameCopy.check_win()
                gameCopy.currentPlayer = 3 - gameCopy.currentPlayer

            if gameCopy.state == self.number:
                possible[firstChoice] += 1
            elif gameCopy.state == 3 - self.number:
                possible[firstChoice] -= 1

            while i > 0:
                gameCopy.undo_move()
                gameCopy.currentPlayer = 3 - gameCopy.currentPlayer
                i -= 1

        print(numGames, sorted(possible.values(), reverse=True)[:10])
        return max(possible, key=lambda x: possible[x])

def evaluate(gameInst):
    values = {
        "Swordsman" : 1,
        "Marksman" : 4,
        "Sapper" : 2,
        "Necromancer" : 1000,
        "Spearman" : 3,
        "Guardian" : 6,
        "Mage" : 2,
        "Berserk" : 5,
        "Mine" : 0
    }

    value = 0

    for y in range(gameInst.height):
        for x in range(gameInst.width):
            if gameInst.is_ally(x, y, 1):
                value += values[type(gameInst.board[y][x]).__name__]

            if gameInst.is_ally(x, y, 2):
                value -= values[type(gameInst.board[y][x]).__name__]

    return value