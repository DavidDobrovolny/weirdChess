import game
import gui

from randomPlayer import RandomPlayer
from greedy import Greedy

from mcts import MCTS
from mctsMem import MCTSMemory
from mctsEC import MCTSEarlyCutout

from negamax import NegamaxPlayer
from negamax2 import NegamaxPlayer2
from negamax2qe import NegamaxPlayer2QE
from negamax2qeKm import NegamaxPlayer2QEKM

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
    p1turns = 0
    p2turns = 0
    p1time = 0
    p2time = 0

    if verbose > 1:
        g = gui.BoardGUI()

    t = time.time()

    for i in range(0, n):
        print(i)
        theGame = game.Game()
        if verbose > 1:
            g.update_board(theGame.board_to_text())

        while theGame.state == -1:
            if verbose > 0:
                value = evaluate(theGame)
                print(value, len(theGame.get_possible_moves()))
            if theGame.currentPlayer == 1:
                turnTime = time.time()

                choice = p1.choose(theGame)

                p1time += time.time() - turnTime
                p1turns += 1
            else:
                turnTime = time.time()

                choice = p2.choose(theGame)

                p2time += time.time() - turnTime
                p2turns += 1

            theGame.make_move(choice)

            if verbose > 1:
                g.update_board(theGame.board_to_text())
                time.sleep(1)

        wins[theGame.state] += 1
        print(wins)

    print(wins, "Time spent:", time.time() - t, "Time spent per game:", (time.time() - t)/n)
    print("Player 1 time spent per turn:", p1time/p1turns)
    print("Player 2 time spent per turn:", p2time/p2turns)

    if verbose > 1: # to keep plot from closing
        input()

player1 = NegamaxPlayer2QEKM(1, d=4)
player2 = NegamaxPlayer2QEKM(2, d=3)

simulate(10, player1, player2, verbose=0)