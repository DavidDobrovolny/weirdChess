import pieceBase
import moveObj

class Swordsman(pieceBase.Piece):
    def __init__(self, x, y, col):
        super().__init__(x, y, col)

    def get_possible_moves(self, game):
        moves = []

        for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if game.is_free(self.x + dx, self.y + dy) and game.is_free(self.x + 2 * dx, self.y + 2 * dy):
                moves.append(moveObj.Move(self, self.x, self.y, self.x + 2 * dx, self.y + 2 * dy))

        for (dx, dy) in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            if game.is_free(self.x + dx, self.y + dy) and (game.is_free(self.x + dx, self.y) or game.is_free(self.x, self.y + dy)):
                moves.append(moveObj.Move(self, self.x, self.y, self.x + dx, self.y + dy))

        # KILL MOVES

        for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if game.is_free(self.x + dx, self.y + dy)\
                    and game.is_enemy(self.x + 2 * dx, self.y + 2 * dy, self.color)\
                    and game.board[self.y + 2 * dy][self.x + 2 * dx].is_killable(game):

                if game.is_free(self.x + 2 * dx + dy, self.y + 2 * dy + dx):
                    killed = game.board[self.y + 2 * dy][self.x + 2 * dx]
                    if type(killed).__name__ == "Mine":
                        killed = (killed, self)
                    else:
                        killed = (killed,)

                    moves.append(
                        moveObj.Move(
                            self,
                            self.x,
                            self.y,
                            self.x + 2 * dx + dy,
                            self.y + 2 * dy + dx,
                            removed = killed
                        ))

                if game.is_free(self.x + 2 * dx - dy, self.y + 2 * dy - dx):
                    killed = game.board[self.y + 2 * dy][self.x + 2 * dx]
                    if type(killed).__name__ == "Mine":
                        killed = (killed, self)
                    else:
                        killed = (killed,)

                    moves.append(
                        moveObj.Move(
                            self,
                            self.x,
                            self.y,
                            self.x + 2 * dx - dy,
                            self.y + 2 * dy - dx,
                            removed = killed
                        ))

        return moves