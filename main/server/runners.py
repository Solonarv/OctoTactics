'''
Created on 06.10.2013

@author: Solonarv
'''


from abc import ABCMeta, abstractmethod
from server.network.listen import ThreadNetworkListener
from struct import Struct
from server.network.events import ClientJoinedEvent
from server.model.board import Board

class BaseServerRunner(metaclass = ABCMeta):
    def __init__(self, server):
        self.server = server
    @abstractmethod
    def load(self): pass

class PregameServerRunner(BaseServerRunner):
    """
    In this phase, players join a game and settings are made, i.e.
    game mode, optional win conditions, teams etc
    """
    def load(self):
        self.netlistener = ThreadNetworkListener(self.server, self.server.port)
        self.server.EVENT_BUS.register(self.onClientJoin, ClientJoinedEvent)
        self.netlistener.start()
        self.server.settings = {}
        self.load_default_settings()
    
    def onClientJoin(self, event):
        msg = self.struct_ClientJoinedBroadcast.pack(event.client.isAI, event.client.cluid, event.client.clientname)
        self.server.clients.broadcast(msg)
    
    def onClientReady(self, event):
        self.server.clients.broadcast(self.struct_ClientReadyBroadcast(event.client.cluid))

class IngameServerRunner(BaseServerRunner):
    """
    In this phase, the actual game is being carried out.
    """
    def load(self):
        settings=self.server.settings
        self.board = Board(settings["board", "width"], settings["board", "height"])