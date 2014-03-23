'''
Created on 04.03.2014

@author: Solonarv
'''

from util import GameSettings
from net import ThreadListenForPlayers

class State(object):
    def __init__(self, server):
        self.server=server

class StateJoining(State):
    def __init__(self, server):
        State.__init__(self, server)
    
    def run(self):
        netlistener=ThreadListenForPlayers(self.server)
        netlistener.run()
    
    def addPlayer(self, player):
        self.server.players+=[player]
        player.conn.sendall(self.settings.encode())
        if len(self.server.players)==1:
            self.settings.ops+=[player]
        if len(self.server.players)>=self.server.maxplayers:
            self.server.setstate(StatePregameLobby)

class StatePregameLobby(State):
    def __init__(self, prevstate):
        State.__init__(self,prevstate.server)
        self.oldnetlistener=prevstate.netlistener # prevent orphaned thread
    
    def run(self):
        self.running=True
        while self.running:
            msg=self.server.owner.conn.recv(4096).split('\n')
            for line in msg:
                for setting in line.split(";"):
                    option, args=setting.split(":")
                    self.server.settings.setoption(option, args)