import pieceBase
import moveObj

class Spearman(pieceBase.Piece):
    def __init__(self, x, y, col, newId=-1):
        super().__init__(x, y, col, newId)

    def get_possible_moves(self, game):
        moves = []

        for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for i in range(1, game.height + game.width):
                if game.is_free(self.x + i*dx, self.y + i*dy):
                    moves.append(moveObj.Move(self, self.x, self.y, self.x + i*dx, self.y + i*dy))
                else:
                    break


        for (dx, dy) in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            if game.is_enemy(self.x + dx, self.y + dy, self.color) and game.board[self.y + dy][self.x + dx].is_killable(game):
                killed = game.board[self.y + dy][self.x + dx]
                if type(killed).__name__ == "Mine":
                    killed = (killed, self)
                else:
                    killed = (killed,)

                moves.append(
                    moveObj.Move(
                        self,
                        self.x,
                        self.y,
                        self.x + dx,
                        self.y + dy,
                        removed=killed
                    )
                )

            if game.is_enemy(self.x + dx, self.y + dy, self.color)\
                    and game.is_free(self.x + 2*dx, self.y + 2*dy)\
                    and game.board[self.y + dy][self.x + dx].is_killable(game):

                killed = game.board[self.y + dy][self.x + dx]
                if type(killed).__name__ == "Mine":
                    killed = (killed, self)
                else:
                    killed = (killed,)

                moves.append(
                    moveObj.Move(
                        self,
                        self.x,
                        self.y,
                        self.x + 2*dx,
                        self.y + 2*dy,
                        removed=killed
                    )
                )

            if game.is_enemy(self.x + 2*dx, self.y + 2*dy, self.color)\
                    and game.is_free(self.x + dx, self.y + dy) \
                    and game.board[self.y + 2*dy][self.x + 2*dx].is_killable(game):

                killed = game.board[self.y + 2*dy][self.x + 2*dx]
                if type(killed).__name__ == "Mine":
                    killed = (killed, self)
                else:
                    killed = (killed,)

                moves.append(
                    moveObj.Move(
                        self,
                        self.x,
                        self.y,
                        self.x + 2*dx,
                        self.y + 2*dy,
                        removed=killed
                    )
                )

        return moves