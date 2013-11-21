'''
Created on 4 nov. 2013

@author: alex
'''

from tkinter import *
from sys import exit
from prototype.model import Board

def onclick(event):
    global focus
    print("canvas onclick called")
    cx=canvas.canvasx(event.x, 30)/30
    cy=canvas.canvasy(event.y, 30)/30
    cell=board.cells[cx,cy]
    if focus is None or (cx-focus.x)**2+(cy-focus.y)**2>=focus.rangeSq:
        focus=cell
        print("Set focus to %i,%i" % (cx,cy))
    elif cell in focus.targets:
        focus.targets.remove(cell)
        print("Cell at %i,%i is no longer targeting cell at %i,%i" % (focus.x,focus.y,cx,cy))
        focus=None
    elif cell==focus:
        focus.targets=[]
        print("Cell at %i,%i is no longer targeting anything" % (cx,cy))
        focus=None
    elif len(focus.targets)<focus.maxTargets:
        focus.targets.append(cell)
        print("Cell at %i,%i is now targeting cell at %i,%i" % (focus.x,focus.y,cx,cy))
        focus=None

def update():
    board.tick()
    board.draw(canvas)
    window.after(50, update)

def startgame():
    launchgame.config(command=0)
    global board
    board=Board(15,10)
    update()


def settings():
    pass

def leavegame():
    exit(0)

window=Tk()
window.title("OctoTactics - Prototype")
window.geometry("640x480")
board=None
focus=None

canvas=Canvas(window, bg="white",width=450,height=300 )
canvas.grid(column=1, row=2, columnspan=3)
canvas.bind("<Button-1>",onclick)


presentation=Label(window, text="Welcome on our first game ever: OctoTactics !")
launchgame=Button(window, text="Play!", command=startgame)
launchgame.grid(column=1, row=1)
settings=Button(window, text="Settings", command=settings)
settings.grid(column=2, row=1)
quitgame=Button(window, text="Quit game - Bad idea!", command=leavegame)
quitgame.grid(column=3, row=1)

window.mainloop()
