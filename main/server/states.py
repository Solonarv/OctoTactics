'''
Created on 04.03.2014

@author: Solonarv
'''

from server.util import GameSettings
from server.net import ThreadListenForPlayers

class State(object):
    def __init__(self, server):
        self.server=server

class StateHasGameSettings(State):
    def __init__(self, server):
        State.__init__(self,server)
        self.settings=GameSettings()

class StateJoining(StateHasGameSettings):
    def __init__(self, server, port):
        StateHasGameSettings.__init__(self, server)
    
    def run(self):
        netlistener=ThreadListenForPlayers(self.server)
        netlistener.run()