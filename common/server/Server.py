'''
Created on 31.07.2013

@author: Solonarv
'''

from abc import ABCMeta, abstractmethod
from util import Enum
from util.events import EventBus
from server.events import *

class ClientConnection(object):
    """
    Used server-side to represent a connection to a client
    """
    
    def __init__(self, stream):
        self.stream = stream
        stream.setblocking(False)
        

class Server(metaclass=ABCMeta):
    '''
    ABC of server
    '''
    
    STATE = Enum(("UNLOADED", "STARTING", "WAITING", "RUNNING", "STOPPING", "STOPPED", "ERRORED",))
    
    def __init__(self, name):
        self.state = Server.STATE.UNLOADED
        self.name = name
        self.EVENT_BUS = EventBus()
    
    def setstate(self, state):
        if self.EVENT_BUS.post(ServerStateEvent(self,state)):
            self.state = state
    
    def game_tick(self):
        self.EVENT_BUS.post(ServerTickEvent(self))
        self.EVENT_BUS.post(ServerPostTickEvent(self))