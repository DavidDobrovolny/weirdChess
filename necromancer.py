import pieceBase
import moveObj

class Necromancer(pieceBase.Piece):
    def __init__(self, x, y, col, newId=-1):
        super().__init__(x, y, col, newId)

    def get_possible_moves(self, game):
        moves = []

        for dx, dy in [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if not (x == y == 0)]:
            if game.is_free(self.x + dx, self.y + dy):
                if self.color == 1:
                    revived = None if len(game.p1graveyard) == 0 else type(game.p1graveyard[0])(self.x, self.y, self.color, game.p1graveyard[0].id)
                else:
                    revived = None if len(game.p2graveyard) == 0 else type(game.p2graveyard[0])(self.x, self.y, self.color, game.p2graveyard[0].id)

                moves.append(moveObj.Move(self, self.x, self.y, self.x + dx, self.y + dy, added=() if revived is None else (revived,)))

        return moves

    def undo_remove(self, game):
        game.board[self.y][self.x] = self

        if self.color == 1:
            game.p1graveyard.pop()
            game.p1necroDead = False

        elif self.color == 2:
            game.p2graveyard.pop()
            game.p2necroDead = False

    def remove(self, game):
        if game.board[self.y][self.x] == self:
            game.board[self.y][self.x] = None

        if self.color == 1:
            game.p1graveyard.append(self)
            game.p1necroDead = True

        elif self.color == 2:
            game.p2graveyard.append(self)
            game.p2necroDead = True