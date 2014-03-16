'''
Created on 04.03.2014

@author: Solonarv
'''

import states
from model import board
import socket

class Server(object):
    def __init__(self,port):
        self.players=[]
        self.port=port
        self.state=states.StateJoining(self)
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('',port))
        self.state.run()
    
    def startgame(self):
        self.board=board.Board()
    
    def setstate(self, stateType):
        oldstate=self.state
        self.state.stop()
        self.state=stateType(self.state)
        oldstate.kill()
        self.state.run()