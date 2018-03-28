import pieceBase
import moveObj

class Marksman(pieceBase.Piece):
    def __init__(self, x, y, col):
        super().__init__(x, y, col)

    def get_possible_moves(self, game):
        moves = []

        for dx, dy in [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if not (x == y == 0)]:
            if game.is_free(self.x + dx, self.y + dy):
                killed = ()

                for i in range(1, game.width + game.height):
                    if game.is_free(self.x - i*dx, self.y - i*dy):
                        continue

                    if game.is_enemy(self.x - i*dx, self.y - i*dy, self.color)\
                            and game.board[self.y - i*dy][self.x - i*dx].is_killable(game):
                        killed = (game.board[self.y - i*dy][self.x - i*dx],)
                        break
                    elif game.is_enemy(self.x - i*dx, self.y - i*dy, self.color) or game.is_ally(self.x - i*dx, self.y - i*dy, self.color):
                        break


                moves.append(moveObj.Move(self, self.x, self.y, self.x + dx, self.y + dy, removed = killed))

        return moves