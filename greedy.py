import copy


class Greedy:
    def __init__(self, num):
        self.number = num

    def choose(self, gameInst):
        gameCopy = copy.deepcopy(gameInst)

        possible = {move: 0 for move in gameInst.get_possible_moves()}

        for move in list(possible.keys()):
            gameCopy.make_move(move)
            possible[move] = evaluate(gameCopy) * (-1 if self.number == 2 else 1)
            gameCopy.undo_move()

        return max(possible, key = lambda x: possible[x])

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