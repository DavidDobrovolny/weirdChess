class Move:
    def __init__(self, piece, oldX, oldY, newX, newY, added = (), removed = (), moved = ()):
        """
        :param piece: moved piece

        :param oldX: old x coordinate
        :param oldY: old y coordinate

        :param newX: new x coordinate
        :param newY: new y coordinate

        :param added: tuple of added pieces
        :param removed: tuple of removed pieces
        :param moved: tuple of Move objects
        """

        self.piece = piece

        self.oldX = oldX
        self.oldY = oldY

        self.newX = newX
        self.newY = newY

        self.added = added
        self.removed = removed
        self.moved = moved

    def __eq__(self, other):
        return (self.piece, self.oldX, self.oldY, self.newX, self.newY, self.added, self.removed, self.moved) ==\
               (other.piece, other.oldX, other.oldY, other.newX, other.newY, other.added, other.removed, other.moved)