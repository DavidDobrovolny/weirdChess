import copy
import random

class NegamaxPlayer2QEKM:
    """
    Negamax with alpha-beta pruning and iterative deepening for move ordering
    Uses quick evaluation
    """

    def __init__(self, num, d=3):
        self.number = num
        self.depth = d
        self.theGame = None
        self.moveTree = None

        self.killers = [[] for _ in range(0, self.depth + 1)]

    def choose(self, gameInst):
        self.theGame = copy.deepcopy(gameInst)
        self.moveTree = Node(None)

        self.killers = [[] for _ in range(0, self.depth + 1)]

        for i in range(1, self.depth+1):
            self.negamax(self.moveTree, i, -100000, 100000, (self.number * 2 - 3), 0)

        random.shuffle(self.moveTree.childMoves)

        return min(self.moveTree.childMoves, key=lambda x: x.value).move

    def negamax(self, node, depth, alpha, beta, color, pValue):
        if self.theGame.state != -1:
            return

        if len(node.childMoves) == 0:
            node.childMoves = [Node(x) for x in self.theGame.get_possible_moves()]

        for killer in self.killers[depth][::-1]:
            if killer in [x.move for x in node.childMoves]:
                node.childMoves.remove([x for x in node.childMoves if x.move == killer][0])
                node.childMoves.insert(0, Node(killer))

        if depth == 1:
            bestMove = None
            bestValue = -100000

            for moveNode in node.childMoves:
                moveNode.value = -evaluate_move(moveNode.move) * color + pValue

                if -moveNode.value > bestValue:
                    bestValue = -moveNode.value
                    bestMove = moveNode

            node.childMoves.remove(bestMove)
            node.childMoves.insert(0, bestMove)

            node.value = bestValue
            return

        bestValue = -100000
        bestMove = None

        for moveNode in node.childMoves:
            self.theGame.make_move(moveNode.move)

            self.negamax(moveNode, depth-1, -beta, -alpha, -color, evaluate_move(moveNode.move) * color + pValue)

            if -moveNode.value > bestValue:
                bestValue = -moveNode.value
                bestMove = moveNode

            alpha = max(alpha, -moveNode.value)
            self.theGame.undo_move()

            if alpha >= beta:
                self.killers[depth].insert(0, moveNode.move)
                if len(self.killers[depth]) > 2:
                    self.killers[depth].pop()
                break

        node.childMoves.remove(bestMove)
        node.childMoves.insert(0, bestMove)

        node.value = bestValue
        return

class Node:
    def __init__(self, m):
        self.move = m
        self.value = -10000
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

def evaluate_move(move):
    values = {
        "Swordsman": 1,
        "Marksman": 4,
        "Sapper": 2,
        "Necromancer": 1000,
        "Spearman": 3,
        "Guardian": 6,
        "Mage": 2,
        "Berserk": 5,
        "Mine": 0
    }

    value = 0

    for piece in move.added:
        value += values[type(piece).__name__] * (1 if piece.color == 1 else -1)

    for piece in move.removed:
        value += values[type(piece).__name__] * (1 if piece.color == 1 else -1)

    return value