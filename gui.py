import matplotlib.pyplot as plt
from PIL import Image

class BoardGUI:
    def __init__(self):
        self.board = Image.new("RGBA", (7 * 50, 7 * 50), color=(255, 255, 255))
        self.plot = plt.imshow(self.board)

        plt.ion()
        plt.show()
        plt.pause(0.05)

    def update_board(self, board):
        images = {
            "f": "swordsman",
            "m": "marksman",
            "s": "sapper",
            "n": "necromancer",
            "p": "spearman",
            "g": "guardian",
            "w": "mage",
            "b": "berserk",
            "o": "mine"
        }

        self.board = Image.new("RGBA", (7 * 50, 7 * 50), color = (255, 255, 255, 255))

        lines = board.split("/")

        for y in range(0, 7):
            for x in range(0, 7):
                if lines[y][x] == ".":
                    image = "empty.png"
                else:
                    color = "W" if lines[y][x].islower() else "B"
                    image = images[lines[y][x].lower()] + color + ".png"

                newImage = Image.open("static/" + image).resize((50, 50))
                self.board.paste(newImage, (x*50, y*50, x*50 + 50, y*50 + 50))

        self.plot.set_data(self.board)
        plt.draw()
        plt.pause(0.05)