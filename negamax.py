import copy

class NegamaxPlayer:
    """
    Negamax with alpha-beta pruning
    """

    def __init__(self, num, d=2):
        self.number = num
        self.depth = d
        self.theGame = None

    def __str__(self):
        return "Negamax depth {0.depth}".format(self)

    def choose(self, gameInst):
        self.theGame = copy.deepcopy(gameInst)

        _, otherMove = self.negamax(self.depth, -100000, 1000000, -(self.number * 2 - 3))
        #moveToMake = [x for x in gameInst.get_possible_moves() if (x.oldX, x.oldY, x.newX, x.newY) == (otherMove.oldX, otherMove.oldY, otherMove.newX, otherMove.newY)][0]

        return otherMove

    def negamax(self, depth, alpha, beta, color):
        if depth == 0 or self.theGame.state != -1:
            value = color * evaluate(self.theGame)
            return value, None

        moves = self.theGame.get_possible_moves()

        bestValue = -100000
        bestMove = None

        for move in moves:
            self.theGame.make_move(move)
            v, _ = self.negamax(depth-1, -beta, -alpha, -color)
            v = -v
            bestValue = max(bestValue, v)
            bestMove = move if v == bestValue else bestMove
            alpha = max(alpha, v)
            self.theGame.undo_move()

            if alpha >= beta:
                break

        return bestValue, bestMove

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