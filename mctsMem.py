import random
import time
import copy


class MCTSMemory:
    """
    Pure Monte Carlo Tree Search with memory
    """

    def __init__(self, num, t=5):
        self.number = num
        self.thinkTime = t

        self.moveTree = self.Node(None, 1, None)

    def choose(self, gameInst):
        gameCopy = copy.deepcopy(gameInst)

        if len(self.moveTree.childMoves) != 0 and gameCopy.moves[-1] in [x.move for x in self.moveTree.childMoves]:
            self.moveTree = [x for x in self.moveTree.childMoves if x.move == gameCopy.moves[-1]][0]
        else:
            self.moveTree = self.Node(None, self.number, None)

        startTime = time.time()

        while time.time() - startTime < self.thinkTime:
            currentMove = self.moveTree
            i = 0

            while len(currentMove.childMoves) != 0:
                currentMove = random.choice(currentMove.childMoves)
                gameCopy.make_move(currentMove.move)
                i += 1

            currentMove.childMoves = [self.Node(x, 3 - currentMove.color, currentMove) for x in gameCopy.get_possible_moves()]

            currentMove = random.choice(currentMove.childMoves)
            gameCopy.make_move(currentMove.move)
            i += 1

            while gameCopy.state == -1:
                choice = random.choice(gameCopy.get_possible_moves())
                gameCopy.make_move(choice)
                i += 1

            win = gameCopy.state != currentMove.color

            currentMove.backpropagate(win)

            while i > 0:
                gameCopy.undo_move()
                i -= 1

        #print(sorted([x.wins for x in self.moveTree.childMoves], reverse=True))
        chosen = max(self.moveTree.childMoves, key=lambda x: x.wins)
        self.moveTree = chosen

        return chosen.move

    def move_to_tuple(self, move):
        return move.oldX, move.oldY, move.newX, move.newY

    class Node:
        def __init__(self, m, c, p):
            self.move = m
            self.color = c
            self.wins = 0
            self.simulations = 0

            self.parent = p
            self.childMoves = []

        def backpropagate(self, win):
            if win:
                self.wins += 1

            self.simulations += 1

            if self.parent is not None:
                self.parent.backpropagate(not win)