'''
Created on 31.07.2013

@author: Solonarv
'''

from abc import ABCMeta, abstractmethod
from util import Enum
from util.events import EventBus
from server.events import *
from threading import Lock
from server.network.listen import ThreadNetworkListener

class ClientConnection(object):
    """
    Used server-side to represent a connection to a client
    """
    
    def __init__(self, stream):
        self.stream = stream
        stream.setblocking(False)
        

class Server(metaclass=ABCMeta):
    STATE = Enum(("UNLOADED", "STARTING", "WAITING", "RUNNING", "STOPPING", "STOPPED", "ERRORED",))
    
    def __init__(self, name, port):
        self.state = Server.STATE.UNLOADED
        self.name = name
        self.EVENT_BUS = EventBus()
        self.connected_clients=[]
        self.clientlist_lock=Lock()
        self.network_listener = ThreadNetworkListener(self, port)
    
    def setstate(self, state):
        if self.EVENT_BUS.post(ServerStateEvent(self,state)):
            self.state = state
    
    def game_tick(self):
        self.EVENT_BUS.post(ServerTickEvent(self))
        self.EVENT_BUS.post(ServerPostTickEvent(self))
        
    def add_client(self, conn):
        with self.clientlist_lock:
            self.connected_clients.append(conn)