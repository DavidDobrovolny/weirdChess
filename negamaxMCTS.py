import copy
import random
import time

class NegamaxMCTSPlayer:
    """
    Negamax - Monte Carlo Tree Search abomination
    """

    def __init__(self, num, d1=3, d2=5, t=10):
        self.number = num
        self.nDepth = d1
        self.mDepth = d2
        self.thinkTime = t
        self.theGame = None
        self.moveTree = None

        self.killers = [[] for _ in range(0, self.nDepth + 1)]

    def __str__(self):
        return "NegamaxMCTS nDepth {0.nDepth}, mDepth {0.mDepth}, thinkTime {0.thinkTime}".format(self)

    def choose(self, gameInst):
        self.theGame = copy.deepcopy(gameInst)
        self.moveTree = Node(None)

        self.killers = [[] for _ in range(0, self.nDepth + 1)]

        # NEGAMAX

        for i in range(1, self.nDepth):
            self.negamax(self.moveTree, i, -100000, 100000, -(self.number * 2 - 3), 0)

        # MCTS

        if self.moveTree.value > 500:  # guaranteed win
            return min(self.moveTree.childMoves, key=lambda x: x.value).move

        gameCopy = copy.deepcopy(gameInst)

        self.moveTree.childMoves.sort(key=lambda x: x.value)
        possible = {move_to_tuple(x.move): [0, 0] for x in self.moveTree.childMoves if -x.value > -500}  # avoid guaranteed losses

        mctsGames = 0
        startTime = time.time()

        if len(possible) == 0:  # guaranteed loss
            return random.choice(self.theGame.get_possible_moves())

        while time.time() - startTime < self.thinkTime:
            firstMove = random.choice(list(possible.keys()))
            gameCopy.make_move(tuple_to_move(firstMove, gameCopy))
            i = 1

            while gameCopy.state == -1 and i < self.mDepth:
                choice = random.choice(gameCopy.get_possible_moves())
                gameCopy.make_move(choice)
                i += 1

            value = evaluate(gameCopy) * (-1 if self.number == 2 else 1)
            possible[firstMove][0] += value
            possible[firstMove][1] += 1

            mctsGames += 1

            while i > 0:
                gameCopy.undo_move()
                i -= 1

        chosen = max(possible, key = lambda x: safe_divide(possible[x][0], possible[x][1]))

        print(mctsGames, "leaves")

        return tuple_to_move(chosen, gameCopy)

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
                moveNode.value = -color * (evaluate_move(moveNode.move) + pValue)

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

            self.negamax(moveNode, depth-1, -beta, -alpha, -color, evaluate_move(moveNode.move) + pValue)

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
        value += values[type(piece).__name__] * (-1 if piece.color == 1 else 1)

    return value