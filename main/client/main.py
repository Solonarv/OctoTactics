'''
Created on 4 nov. 2013

@author: alex
'''

from Tkinter import *
from sys import exit
from model.board import Board
from client.render.render import RenderBoard,ClientPlayer

nil=ClientPlayer("RA","minimal")
me=ClientPlayer("You","magic")


def startgame():
    launchgame.config(command=0)
    global board,renderer
    board=Board(15,10,nil)
    board.cells[0,0].owner=me
    renderer=RenderBoard(board,canvas,me)
    
def donextturn():
    board.tick()
    renderer.update()
    

def settings():
    pass

def leavegame():
    exit(0)

window=Tk()
window.title("OctoTactics")
window.geometry("640x480")
board=None
renderer=None

canvas=Canvas(window, bg="white",width=450,height=300 )
canvas.grid(column=1, row=2, columnspan=3)

launchgame=Button(window, text="Play!", command=startgame)
launchgame.grid(column=1, row=1)
settings=Button(window, text="Settings", command=settings)
settings.grid(column=2, row=1)
quitgame=Button(window, text="Ragequit", command=leavegame)
quitgame.grid(column=3, row=1)
nextturn=Button(window, text="Next Turn",command=donextturn)
nextturn.grid(column=4, row=1)

window.mainloop()
