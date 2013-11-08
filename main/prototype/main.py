'''
Created on 4 nov. 2013

@author: alex
'''

from tkinter import *
import sys

def startgame():
    pass

def settings():
    pass

def leavegame():
    sys.exit(0)

window=Tk()
window.title("OctoTactics - Prototype")
window.geometry("640x480")
canvas=Canvas(window, bg="black", )

presentation=Label(window, text="Welcome on our first game ever: OctoTactics !")

launchgame=Button(window, text="Play!", command=startgame)
launchgame.grid(row=1,column=1)
settings=Button(window, text="Settings", command=settings)
settings.grid(row=2,column=1)
quitgame=Button(window, text="Quit game - Bad idea!", command=leavegame)
quitgame.grid(row=3,column=1)