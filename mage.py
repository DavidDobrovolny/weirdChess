import pieceBase
import moveObj
import copy

class Mage(pieceBase.Piece):
    def __init__(self, x, y, col):
        super().__init__(x, y, col)

    def get_possible_moves(self, game):
        moves = []

        for (dx, dy) in [(x, y) for x in range(-5, 6) for y in range(-5, 6) if abs(x) + abs(y) <= 4 and not (x == y == 0)]:
            if not game.is_in_bounds(self.x + dx, self.y + dy):
                continue

            movedR = () if game.is_free(self.x + dx, self.y + dy) else\
                (moveObj.Move(game.board[self.y + dy][self.x + dx], self.x + dx, self.y + dy, self.x, self.y),)

            # if movedR == ():
            #     movedA = ()
            #
            # else:
            #     movedA = (copy.copy(movedR[0]),)
            #
            #     movedA[0].x = self.x
            #     movedA[0].y = self.y

            moves.append(
                moveObj.Move(
                    self,
                    self.x,
                    self.y,
                    self.x + dx,
                    self.y + dy,
                    moved=movedR
                )
            )

        return moves