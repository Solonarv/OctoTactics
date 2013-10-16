'''
Created on 31.07.2013

@author: Solonarv
'''

from util import Enum
from util.events import EventBus
from server.events import *
from threading import Lock
from server.network.listen import ThreadNetworkListener
from server.network.persist import ClientList
from server.runners import PregameServerRunner
        

class Server:
    STATE = Enum(("UNLOADED", "STARTING", "WAITING", "RUNNING", "STOPPING", "STOPPED", "ERRORED",))
    
    def __init__(self, name, port):
        self.state = Server.STATE.UNLOADED
        self.name = name
        self.port = port
        self.EVENT_BUS = EventBus()
        self.clients = ClientList()
        self.runner = PregameServerRunner()
    
    def setstate(self, state):
        if self.EVENT_BUS.post(ServerStateEvent(self,state)):
            self.state = state
    
    def game_tick(self):
        self.EVENT_BUS.post(ServerTickEvent(self))
        self.EVENT_BUS.post(ServerPostTickEvent(self))