'''
Created on 04.03.2014

@author: Solonarv
'''

import states
from model import board
import socket
from util import GameSettings

class Server(object):
    def __init__(self,port, maxplayers):
        self.players=[]
        self.owner=None
        self.settings=GameSettings()
        self.maxplayers=maxplayers
        self.port=port
        self.statetype=states.StateJoining
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('',port))
    
    def startgame(self):
        self.board=board.Board()
    
    def run(self):
        self.state=states.StateJoining(self)
        self.state.run()
        while True:
            self.state.stop()
            os=self.state
            self.state=self.statetype(os)
            os.kill()
            self.state.run()
    
    def setstate(self, stateType):
        self.statetype=stateType