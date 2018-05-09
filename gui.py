import os
import datetime
import random
import tkinter
from PIL import Image, ImageTk

import game

from randomPlayer import RandomPlayer
from negamax2qeKm import NegamaxPlayer2QEKM


window = tkinter.Tk()
buttons = [[None for _ in range(0, 7)] for _ in range(0, 7)]

images = {}
imageNames = os.listdir("static")
for imageName in imageNames:
    im = Image.open("static/" + imageName).resize((50, 50))
    images[imageName[:-4]] = ImageTk.PhotoImage(im)

for y in range(0, 7):
    for x in range(0, 7):
        buttons[y][x] = tkinter.Button(window, image=images["empty"], width=50, height=50, bg="beige", command=lambda x=x, y=y: click(x, y))
        buttons[y][x].grid(row=y, column=x+1)

p1graveyard = tkinter.Label(window, width=20, height=25, text="White graveyard", anchor="n")
p2graveyard = tkinter.Label(window, width=20, height=25, text="Black graveyard", anchor="n")

p1graveyard.grid(row=0, column=0, rowspan=7)
p2graveyard.grid(row=0, column=8, rowspan=7)

def click(x, y):
    global selected, moves

    if selected == (-1, -1) and (x, y) in moves.keys():
        selected = (x, y)
        select(x, y)

    elif selected != (-1, -1) and (x, y) in moves[selected]:
        deselect(*selected)
        move(*selected, x, y)
        selected = (-1, -1)

        window.update()
        if theGame.state == -1:
            window.after(500, ai_move())

    elif selected != (-1, -1):
        deselect(*selected)
        selected = (-1, -1)

def select(x, y):
    buttons[y][x].configure(bg="light green")

    for tile in moves[(x, y)]:
        buttons[tile[1]][tile[0]].configure(bg="orange")

def deselect(x, y):
    buttons[y][x].configure(bg = "beige")

    for tile in moves[(x, y)]:
        buttons[tile[1]][tile[0]].configure(bg = "beige")

def move(x1, y1, x2, y2):
    global moves

    theGame.make_move(theGame.string_to_move(theGame.tuple_to_string((x1, y1, x2, y2))))
    update_board()
    moves = theGame.moves_to_dict()

def ai_move():
    global moves
    theGame.make_move(AI.choose(theGame))
    moves = theGame.moves_to_dict()
    update_board()

def update_board():
    board = theGame.board_to_text()
    lines = board.split("/")

    imageChars = {
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

    for y in range(0, 7):
        for x in range(0, 7):
            if lines[y][x] == ".":
                image = "empty"
            else:
                color = "W" if lines[y][x].islower() else "B"
                image = imageChars[lines[y][x].lower()] + color

            buttons[y][x].configure(image=images[image])

    p1graveyard.configure(text="White graveyard\n" + "\n".join([type(x).__name__ for x in theGame.p1graveyard]))
    p2graveyard.configure(text="Black graveyard\n" + "\n".join([type(x).__name__ for x in theGame.p2graveyard]))

    if theGame.state != -1:
        end_game()

def end_game():
    currentTime = datetime.datetime.today()

    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open("logs/log_{0.year}_{0.month}_{0.day}_{0.hour}_{0.minute}_{0.second}.txt".format(currentTime), "w") as f:
        f.write(str(start))
        f.write("\n")

        f.write(str(theGame.state))
        f.write("\n")

        for m in theGame.moves:
            f.write("{0.oldX}x{0.oldY}/{0.newX}x{0.newY}\n".format(m))


theGame = game.Game()

moves = theGame.moves_to_dict()
selected = (-1, -1)

start = random.choice((1, 2))

AI = NegamaxPlayer2QEKM(start, d=1)

update_board()
window.update()

if start == 1:
    window.after(500, ai_move())

window.mainloop()