import pieceBase
import moveObj

from swordsman import Swordsman
from marksman import Marksman
from sapper import Sapper
from necromancer import Necromancer
from spearman import Spearman
from guardian import Guardian
from mage import Mage
from berserk import Berserk

import json

class Game:
    def __init__(self):
        self.board = []

        self.build_board()

        self.width = len(self.board[0])
        self.height = len(self.board)

        self.currentPlayer = 1

        self.p1graveyard = []
        self.p2graveyard = []

        self.p1necroDead = False
        self.p2necroDead = False

        self.state = -1  # -1 - in progress, 0 - draw, 1/2 - win
        self.moves = []

    def build_board(self):
        with open("plan2.txt", "r") as plan:
            planTxt = plan.readlines()
            planTxt = [line.replace(" ", "")[:-1] for line in planTxt]

        pieceDict = {
            "s": Swordsman,
            "m": Marksman,
            "S": Sapper,
            "N": Necromancer,
            "1": Spearman,
            "g": Guardian,
            "M": Mage,
            "b": Berserk
        }

        self.board = [[None for _ in range(0, len(planTxt[0]))] for _ in range(0, len(planTxt))]

        for y in range(len(planTxt)):
            for x in range(len(planTxt[0])):
                if self.board[y][x] is not None or planTxt[y][x] == ".":
                    continue
                self.board[y][x] = pieceDict[planTxt[y][x]](x, y, 2)
                self.board[len(planTxt) - y - 1][len(planTxt[0]) - x - 1] = pieceDict[planTxt[y][x]](len(planTxt[0]) - x - 1, len(planTxt) - y - 1, 1)

    def get_possible_moves(self):
        moves = []

        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.board[y][x] is not None and self.board[y][x].color == self.currentPlayer:
                    moves.extend(self.board[y][x].get_possible_moves(self))

        return moves

    def make_move(self, move):
        """
        Makes given move.

        :param move: Move object
        :return: None
        """

        possible = self.get_possible_moves()

        if all([x != move for x in possible]):
            print(move.piece)
            raise ValueError("Invalid move")

        self.moves.append(move)

        move.piece.move(self, move)

        for moved in move.moved:
            moved.piece.move(self, moved)

        for piece in move.removed:
            piece.remove(self)

        for piece in move.added:
            piece.add(self)

        self.currentPlayer = 3 - self.currentPlayer
        self.check_win()

    def undo_move(self):
        """
        Undoes last move.

        :return: None
        """
        move = self.moves.pop()

        move.piece.undo_move(self, move)

        for piece in move.added:
            piece.undo_add(self)

        for piece in move.removed:
            piece.undo_remove(self)

        for moved in move.moved:
            moved.piece.undo_move(self, moved)

        self.currentPlayer = 3 - self.currentPlayer
        self.state = -1

    def is_in_bounds(self, x, y):
        """
        Checks whether tile (x, y) is in bounds of board

        :param x: x coordinate
        :param y: y coordinate
        :return: True if in bounds, False if out of bounds
        """

        return 0 <= x < self.width and 0 <= y < self.height

    def is_free(self, x, y):
        """
        Checks whether tile (x, y) is free

        :param x: x coordinate
        :param y: y coordinate
        :return: True if free, False if not free or out of bounds
        """

        return self.is_in_bounds(x, y) and self.board[y][x] is None

    def is_enemy(self, x, y, col):
        """
        Checks whether tile (x, y) is enemy to col

        :param x: x coordinate
        :param y: y coordinate
        :param col: color to check
        :return: True if enemy, False if not or out of bounds
        """

        return self.is_in_bounds(x, y) and self.board[y][x] is not None and self.board[y][x].color != col

    def is_ally(self, x, y, col):
        """
        Checks whether tile (x, y) is ally to col

        :param x: x coordinate
        :param y: y coordinate
        :param col: color to check
        :return: True if ally, False if not or out of bounds
        """

        return self.is_enemy(x, y, 3 - col)

    def check_win(self):
        """
        Checks whether any player won and updates state of game

        :return: None
        """

        if len(self.get_possible_moves()) == 0 or (self.p1necroDead and self.p2necroDead):
            self.state = 0

        if self.p1necroDead:
            self.state = 2

        if self.p2necroDead:
            self.state = 1

    # SERVER STUFF

    def board_to_text(self):
        """
        Converts board to text representation.

        :return: string
        """

        pieceDict = {
            "Swordsman": "f",
            "Marksman": "m",
            "Sapper" : "s",
            "Necromancer" : "n",
            "Spearman" : "p",
            "Guardian": "g",
            "Mage" : "w",
            "Berserk" : "b",
            "Mine" : "o"
        }

        text = ""

        for y in range(0, self.height):
            for x in range(0, self.width):  # for every tile

                if self.board[y][x] is not None:
                    piece = pieceDict[type(self.board[y][x]).__name__]
                    if self.board[y][x].color == 2:
                        piece = piece.upper()
                else:
                    piece = "."

                text += piece

            text += "/"

        return text[:-1]

    def moves_to_dict(self):
        """
        Converts possible moves to dictionary

        :return: (start coordinates) : [(end coordinates)]
        """

        moves = self.get_possible_moves()

        movesDict = {}

        for move in moves:
            if (move.oldX, move.oldY) not in movesDict.keys():
                movesDict[(move.oldX, move.oldY)] = []

            movesDict[(move.oldX, move.oldY)].append((move.newX, move.newY))

        return movesDict

    def moves_to_json(self):
        """
        Converts possible moves to json

        :return: json (start coordinates) : [(end coordinates)]
        """

        moves = self.get_possible_moves()

        movesDict = {}

        for move in moves:
            if str(move.oldX) + "x" + str(move.oldY) not in movesDict.keys():
                movesDict[str(move.oldX) + "x" + str(move.oldY)] = []

            movesDict[str(move.oldX) + "x" + str(move.oldY)].append(str(move.newX) + "x" + str(move.newY))

        return json.dumps(movesDict)

    def tuple_to_string(self, t):
        return str(t[0]) + "x" + str(t[1]) + "/" + str(t[2]) + "x" + str(t[3])

    def string_to_move(self, moveStr):
        old, new = moveStr.split("/")
        oldX, oldY = old.split("x")
        newX, newY = new.split("x")

        oldX = int(oldX)
        oldY = int(oldY)
        newX = int(newX)
        newY = int(newY)

        for move in self.get_possible_moves():
            if oldX == move.oldX and oldY == move.oldY and newX == move.newX and newY == move.newY:
                return move
