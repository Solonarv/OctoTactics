'''
Created on 4 nov. 2013

@author: alex
'''
from tkinter import *

def startgame():
    pass

def settings():
    pass

def leavegame():
    import sys
    sys.exit(0)

window=Tk()
window.title("OctoTactics - Prototype")
window.geometry("640x480")
canvas=Canvas(window, bg="black", )

presentation=Label(window, text="Welcome on our first game ever: OctoTactics !")

launchgame=Button(window, text="Play!", command=startgame)
settings=Button(window, text="Settings", command=settings)
quitgame=Button(window, text="Quit game - Bad idea!", command=leavegame)