'''
Created on 04.03.2014

@author: Solonarv
'''

from server import states
from model import board
from sys import argv
import socket

class Server(object):
    def __init__(self,port):
        self.players=[]
        self.port=port
        self.state=states.StateJoining(self)
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind('',port)
    
    def startgame(self):
        self.board=board.Board()
    
    def setstate(self, stateType):
        oldstate=self.state
        self.state.stop()
        self.state=stateType(self.state)
        oldstate.kill()
        self.state.run()