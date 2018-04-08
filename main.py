import game

from randomPlayer import RandomPlayer
from greedy import Greedy
from mcts import MCTS
from mctsMem import MCTSMemory
from negamax import NegamaxPlayer

import time

def evaluate(gameInst):
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

    for y in range(gameInst.height):
        for x in range(gameInst.width):
            if gameInst.is_ally(x, y, 1):
                value += values[type(gameInst.board[y][x]).__name__]

            if gameInst.is_ally(x, y, 2):
                value -= values[type(gameInst.board[y][x]).__name__]

    return value

def simulate(n, p1, p2, verbose=0):
    wins = [0, 0, 0]

    t = time.time()

    for i in range(0, n):
        print(i)
        theGame = game.Game()

        while theGame.state == -1:
            if verbose > 0:
                value = evaluate(theGame)
                print(value)
            if theGame.currentPlayer == 1:

                choice = p1.choose(theGame)
            else:
                choice = p2.choose(theGame)

            theGame.make_move(choice)

        wins[theGame.state] += 1

    print(wins, "Time spent:", time.time() - t, "Time spent per game:", (time.time() - t)/n)

player1 = RandomPlayer(1)
player2 = MCTSMemory(2, t=5)

simulate(1, player1, player2, verbose=1)