'''
Created on 4 nov. 2013

@author: alex
'''

from Tkinter import Tk, Canvas, Button, Label
from sys import exit
from os import chdir

from client.render.render import RenderBoard, ClientPlayer
from model.board import Board

chdir("..")

Players={
    "ra"       : ClientPlayer("ra","tech","black"),
    "Solonarv" : ClientPlayer("Solonarv","steampunk","blue"),
    "Guest"    : ClientPlayer("Guest","magic","red")
}


def startgame():
    #launchgame.config(command=0)
    global board,renderer
    board=Board(15,10,Players["ra"])
    board.cells[0,0].owner=board.cells[0,9].owner=Players["Solonarv"]
    board.cells[14,0].owner=board.cells[14,9].owner=Players["Guest"]
    for player in Players.values():
        player.reloadtexpack(window)
    renderer=RenderBoard(board,canvas,Players["Solonarv"],Players["Guest"])
    
    
def donextturn():
    board.tick()
    renderer.update()
    counts=board.countcells()
    if winner!=None:
        winnerlabel.config(text="Player %s won." % winner.name)
        

def settings():
    pass

def leavegame():
    exit(0)

window=Tk()
window.title("OctoTactics")
window.geometry("1024x768")
board=None
renderer=None

canvas=Canvas(window, bg="black",width=770,height=520 )
canvas.grid(column=1, row=2, columnspan=3)

#launchgame=Button(window, text="Play!", command=startgame)
#launchgame.grid(column=1, row=1)
settings=Button(window, text="Settings", command=settings)
settings.grid(column=1, row=1)
quitgame=Button(window, text="Ragequit", command=leavegame)
quitgame.grid(column=2, row=1)
nextturn=Button(window, text="Next Turn",command=donextturn)
nextturn.grid(column=3, row=1)
winnerlabel=Label(window, text="No winner yet")
winnerlabel.grid(row=2,column=4)


startgame()

window.mainloop()
