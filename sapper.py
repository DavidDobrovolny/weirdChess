import pieceBase
import moveObj

class Sapper(pieceBase.Piece):
    def __init__(self, x, y, col):
        super().__init__(x, y, col)

    def move(self, game, move):
        game.board[move.newY][move.newX] = self
        if game.board[self.y][self.x] == self:
            game.board[self.y][self.x] = None

        self.x = move.newX
        self.y = move.newY

    def undo_move(self, game, move):
        game.board[move.oldY][move.oldX] = self
        if game.board[self.y][self.x] == self:
            game.board[self.y][self.x] = None

        self.x = move.oldX
        self.y = move.oldY

    def get_possible_moves(self, game):
        moves = []

        mine = self.find_mine(game)

        for y in range(0, game.height):
            for x in range(0, game.width):
                if game.is_free(x, y):
                    moves.append(
                        moveObj.Move(self,
                                     self.x,
                                     self.y,
                                     x,
                                     y,
                                     added=(Mine(self.x, self.y, self.color),),
                                     removed=(mine,) if mine is not None else tuple()
                                     ))

        return moves

    def find_mine(self, game):
        """
        Finds sapper's mine

        :param game: game instance
        :return: mine object
        """

        for y in range(0, game.height):
            for x in range(0, game.width):
                if game.board[y][x] is not None and type(game.board[y][x]).__name__ == "Mine" and game.board[y][x].color == self.color:
                    return game.board[y][x]
        return None

class Mine(pieceBase.Piece):
    def __init__(self, x, y, col):
        super().__init__(x, y, col)

    def get_possible_moves(self, game):
        moves = []

        for (dx, dy) in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            if game.is_enemy(self.x + dx, self.y + dy, self.color)\
                    and game.board[self.y + dy][self.x + dx].is_killable(game):
                moves.append(
                    moveObj.Move(self, self.x, self.y, self.x + dx, self.y + dy, removed=(game.board[self.y + dy][self.x + dx],))
                )

        return moves

    def move(self, game, move):
        if game.board[self.y][self.x] == self:
            game.board[self.y][self.x] = None

        self.x = move.newX
        self.y = move.newY

    def undo_move(self, game, move):
        game.board[move.oldY][move.oldX] = self

        self.x = move.oldX
        self.y = move.oldY

    def add(self, game):
        game.board[self.y][self.x] = self

    def remove(self, game):
        if game.board[self.y][self.x] == self:
            game.board[self.y][self.x] = None