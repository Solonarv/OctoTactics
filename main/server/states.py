'''
Created on 04.03.2014

@author: Solonarv
'''

from util import GameSettings
from net import ThreadListenForPlayers

class State(object):
    def __init__(self, server):
        self.server=server

class StateHasGameSettings(State):
    def __init__(self, server):
        State.__init__(self,server)
        self.settings=GameSettings()

class StateJoining(StateHasGameSettings):
    def __init__(self, server):
        StateHasGameSettings.__init__(self, server)
    
    def run(self):
        netlistener=ThreadListenForPlayers(self.server)
        netlistener.run()
    
    def addPlayer(self, player):
        self.server.players+=[player]
        player.conn.sendall(self.settings.encode())