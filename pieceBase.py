class Piece:
    def __init__(self, x, y, col):
        """
        Piece base object

        :param x: x coordinate
        :param y: y coordinate
        :param col: color of piece, 1/2
        """

        self.x = x
        self.y = y
        self.color = col

    def get_possible_moves(self, game):
        """
        Returns all possible moves for this piece.

        :param game: game instance
        :return: list of Move objects
        """
        return []

    def is_killable(self, game):
        """
        Checks whether piece is killable

        :param game: game instance
        :return: True if killable, else False
        """

        for dx, dy in [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if not (x == y == 0)]:
            if game.is_ally(self.x + dx, self.y + dy, self.color):
                if type(game.board[self.y + dy][self.x + dx]).__name__ == "Guardian":
                    return False

        return True

    def move(self, game, move):
        """
        Moves piece to x, y

        :param game: game instance
        :param move: move object
        :return: None
        """

        game.board[move.newY][move.newX] = self
        if game.board[self.y][self.x] == self:
            game.board[self.y][self.x] = None

        self.x = move.newX
        self.y = move.newY

    def undo_move(self, game, move):
        """
        Undoes moving

        :param game: game instance
        :param move: move object
        :return: None
        """

        game.board[move.oldY][move.oldX] = self
        if game.board[self.y][self.x] == self:
            game.board[self.y][self.x] = None

        self.x = move.oldX
        self.y = move.oldY

    def add(self, game):
        """
        Adds this piece.

        :param game: game instance
        :param fromGraveyard: should piece be pulled from graveyard
        :return: None
        """

        game.board[self.y][self.x] = self

        if self.color == 1:
            game.p1graveyard.pop(0)

        elif self.color == 2:
            game.p2graveyard.pop(0)

    def remove(self, game):
        """
        Removes this piece.

        :param game: game instance
        :param toGraveyard: should piece be added to graveyard
        :return: None
        """

        if game.board[self.y][self.x] == self:
            game.board[self.y][self.x] = None

        if self.color == 1:
            game.p1graveyard.append(self)

        elif self.color == 2:
            game.p2graveyard.append(self)
