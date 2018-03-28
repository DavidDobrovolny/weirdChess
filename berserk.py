import pieceBase
import moveObj

class Berserk(pieceBase.Piece):
    def __init__(self, x, y, col):
        super().__init__(x, y, col)

    def get_possible_moves(self, game):
        moves = []

        for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if not game.is_free(self.x + dx, self.y + dy):
                continue

            if game.is_free(self.x + 2*dx, self.y + 2*dy):
                moves.append(moveObj.Move(self, self.x, self.y, self.x + 2*dx, self.y + 2*dy))

            if game.is_ally(self.x + 2*dx, self.y + 2*dy, self.color) or game.is_enemy(self.x + 2*dx, self.y + 2*dy, self.color):
                first = game.board[self.y + 2*dy][self.x + 2*dx]

                if type(first).__name__ == "Mine":
                    killed = (first, self)
                else:
                    killed = (first,)

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

                if type(first).__name__ == "Mine":
                    continue

                if game.is_in_bounds(self.x + 3*dx, self.y + 3*dy):
                    second = () if game.is_free(self.x + 3*dx, self.y + 3*dy) else (game.board[self.y + 3*dy][self.x + 3*dx],)

                    if len(second) > 0 and type(second[0]).__name__ == "Mine":
                        killed = (first, second[0], self)
                    else:
                        killed = (first,) + second

                    moves.append(
                        moveObj.Move(
                            self,
                            self.x,
                            self.y,
                            self.x + 3 * dx,
                            self.y + 3 * dy,
                            removed = killed
                        )
                    )

                for lr in (1, -1):  # left right
                    if game.is_in_bounds(self.x + 3*dx + lr*dy, self.y + 3*dy + lr*dx):
                        second = () if game.is_free(self.x + 3*dx + lr*dy, self.y + 3*dy + lr*dx)\
                            else (game.board[self.y + 3*dy + lr*dx][self.x + 3*dx + lr*dy],)

                        if len(second) > 0 and type(second[0]).__name__ == "Mine":
                            killed = (first, second[0], self)
                        else:
                            killed = (first,) + second

                        moves.append(
                            moveObj.Move(
                                self,
                                self.x,
                                self.y,
                                self.x + 3 * dx + lr*dy,
                                self.y + 3 * dy + lr*dx,
                                removed = killed
                            )
                        )

                    if game.is_in_bounds(self.x + 2 * dx + lr * dy, self.y + 2 * dy + lr * dx):
                        second = () if game.is_free(self.x + 2 * dx + lr * dy, self.y + 2 * dy + lr * dx) \
                            else (game.board[self.y + 2 * dy + lr * dx][self.x + 2 * dx + lr * dy],)

                        if len(second) > 0 and type(second[0]).__name__ == "Mine":
                            killed = (first, second[0], self)
                        else:
                            killed = (first,) + second

                        moves.append(
                            moveObj.Move(
                                self,
                                self.x,
                                self.y,
                                self.x + 2 * dx + lr * dy,
                                self.y + 2 * dy + lr * dx,
                                removed = killed
                            )
                        )


        return moves