'''
Created on 4 nov. 2013

@author: alex
'''

from tkinter import *
from sys import exit
from prototype.model import Board
from prototype.render import RenderBoard

def update():
    board.tick()
    renderer.update()
    window.after(50, update)

def startgame():
    launchgame.config(command=0)
    global board,renderer
    board=Board(15,10)
    renderer=RenderBoard(board,canvas)
    update()


def settings():
    pass

def leavegame():
    exit(0)

window=Tk()
window.title("OctoTactics - Prototype")
window.geometry("640x480")
board=None
renderer=None

canvas=Canvas(window, bg="white",width=450,height=300 )
canvas.grid(column=1, row=2, columnspan=3)
#canvas.bind("<Button-1>",onclick)


presentation=Label(window, text="Welcome on our first game ever: OctoTactics !")
launchgame=Button(window, text="Play!", command=startgame)
launchgame.grid(column=1, row=1)
settings=Button(window, text="Settings", command=settings)
settings.grid(column=2, row=1)
quitgame=Button(window, text="Quit game - Bad idea!", command=leavegame)
quitgame.grid(column=3, row=1)

window.mainloop()
