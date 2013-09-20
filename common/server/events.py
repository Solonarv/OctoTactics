'''
Created on 20.09.2013

@author: Solonarv
'''
from util.events import Event

class ServerEvent(Event):
    def __init__(self, server):
        self._server = server

class PreInitializationEvent(ServerEvent): pass

class InitializationEvent(ServerEvent): pass

class PostInitializationEvent(ServerEvent): pass

class ServerStateEvent(ServerEvent):
    def __init__(self, server, state):
        super().__init__(server)
        self.state = state

class ServerTickEvent(ServerEvent): pass

class ServerPostTickEvent(ServerTickEvent): pass