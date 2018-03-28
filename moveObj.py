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