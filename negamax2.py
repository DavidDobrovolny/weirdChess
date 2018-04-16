import copy

class NegamaxPlayer2:
    """
    Negamax with alpha-beta pruning and iterative deepening for move ordering
    """

    def __init__(self, num, d=4):
        self.number = num
        self.depth = d
        self.theGame = None
        self.moveTree = None

    def choose(self, gameInst):
        self.theGame = copy.deepcopy(gameInst)
        self.moveTree = Node(None, self.number)

        for i in range(1, self.depth+1):
            self.negamax(self.moveTree, i, -100000, 100000, (self.number * 2 - 3))

        return max(self.moveTree.childMoves, key=lambda x: x.value).move

    def negamax(self, node, depth, alpha, beta, color):
        if depth == 0 or self.theGame.state != -1:
            value = color * evaluate(self.theGame)
            node.value = value
            return

        if len(node.childMoves) == 0:
            node.childMoves = [Node(x, -color) for x in self.theGame.get_possible_moves()]

        bestValue = -100000
        bestMove = None

        for moveNode in node.childMoves:
            self.theGame.make_move(moveNode.move)
            if moveNode not in node.childMoves:
                node.childMoves.append(moveNode)

            self.negamax(moveNode, depth-1, -beta, -alpha, -color)

            if -moveNode.value > bestValue:
                bestValue = -moveNode.value
                bestMove = moveNode

            alpha = max(alpha, -moveNode.value)
            self.theGame.undo_move()

            if alpha >= beta:
                break

        node.childMoves.remove(bestMove)
        node.childMoves.insert(0, bestMove)

        node.value = bestValue

        return

class Node:
    def __init__(self, m, c):
        self.move = m
        self.color = c
        self.value = 0
        self.childMoves = []

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