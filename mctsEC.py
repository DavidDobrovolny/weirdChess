import random
import time
import copy


class MCTSEarlyCutout:
    """
    Pure Monte Carlo Tree Search with memory
    """

    def __init__(self, num, t=10, d=10):
        self.number = num
        self.thinkTime = t
        self.depth = d

    def choose(self, gameInst):
        gameCopy = copy.deepcopy(gameInst)

        startTime = time.time()
        possible = {move_to_tuple(x):[0, 0] for x in gameCopy.get_possible_moves()}

        while time.time() - startTime < self.thinkTime:
            firstMove = random.choice(list(possible.keys()))
            gameCopy.make_move(tuple_to_move(firstMove, gameCopy))
            i = 1

            while gameCopy.state == -1 and i < self.depth:
                choice = random.choice(gameCopy.get_possible_moves())
                gameCopy.make_move(choice)
                i += 1

            value = evaluate(gameCopy) * (-1 if self.number == 2 else 1)
            possible[firstMove][0] += value
            possible[firstMove][1] += 1

            while i > 0:
                gameCopy.undo_move()
                i -= 1

        chosen = max(possible, key=lambda x: safe_divide(possible[x][0], possible[x][1]))
        #print(possible)

        return tuple_to_move(chosen, gameCopy)

def safe_divide(a, b):
    if b == 0:
        return 0
    else:
        return a/b

def move_to_tuple(move):
    return move.oldX, move.oldY, move.newX, move.newY

def tuple_to_move(move, game):
    m = [x for x in game.get_possible_moves() if move_to_tuple(x) == move]
    return m[0]

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