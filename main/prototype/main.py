'''
Created on 4 nov. 2013

@author: alex
'''

from tkinter import *
from sys import exit

def startgame():
    pass

def settings():
    pass

def leavegame():
    exit(0)

window=Tk()
window.title("OctoTactics - Prototype")
window.geometry("640x480")
canvas=Canvas(window, bg="black", )

presentation=Label(window, text="Welcome on our first game ever: OctoTactics !")
launchgame=Button(window, text="Play!", command=startgame); launchgame.grid(column=1, row=1)
settings=Button(window, text="Settings", command=settings); launchgame.grid(column=2, row=1)
quitgame=Button(window, text="Quit game - Bad idea!", command=leavegame); launchgame.grid(column=3, row=1)

window.mainloop()
