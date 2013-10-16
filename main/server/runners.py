'''
Created on 06.10.2013

@author: Solonarv
'''


from abc import ABCMeta, abstractmethod
from server.network.listen import ThreadNetworkListener
from struct import Struct
from server.network.events import ClientJoinedEvent

class BaseServerRunner(metaclass = ABCMeta):
    def __init__(self, server):
        self.server = server
    @abstractmethod
    def run(self): pass

class PregameServerRunner(BaseServerRunner):
    """
    In this phase, players join a game and settings are made, i.e.
    game mode, optional win conditions, teams etc
    """
    def run(self):
        self.netlistener = ThreadNetworkListener(self.server, self.server.port)
        self.server.EVENT_BUS.register(self.onClientJoin, ClientJoinedEvent)
        self.netlistener.start()
    
    def onClientJoin(self, event):
        msg = self.struct_ClientJoinedBroadcast.pack(event.client.isAI, event.client.cluid, event.client.clientname)
        self.server.clients.broadcast(msg)
    
    def onClientReady(self, event):
        self.server.clients.broadcast(self.struct_ClientReadyBroadcast(event.client.cluid))