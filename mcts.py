import random
import time
import copy


class MCTS:
    """
    Pure Monte Carlo Tree Search
    """

    def __init__(self, num, t=15):
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

            i = 1

            while gameCopy.state == -1:
                choice = random.choice(gameCopy.get_possible_moves())
                i += 1

                gameCopy.make_move(choice)

            if gameCopy.state == self.number:
                possible[firstChoice] += 1

            while i > 0:
                gameCopy.undo_move()
                i -= 1

        return max(possible, key=lambda x: possible[x])