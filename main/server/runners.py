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

class JoiningServerRunner(BaseServerRunner):
    """
    The only phase during which players can join a game
    
    Note: maybe merge with PregameLobbyServerRunner?
    """
    struct_ClientJoinedBroadcast = Struct(">?Q32s")
    # Is it an AI?
    # The client's UID
    # The client's name (32char string)
    def run(self):
        self.listener = ThreadNetworkListener(self.server, self.server.port)
        self.listener.start()
        self.server.EVENT_BUS.register(self.onClientJoin, ClientJoinedEvent)
    
    def onClientJoin(self, event):
        self.server.clients.broadcast()

class PregameLobbyServerRunner(BaseServerRunner):
    """
    Game mode etc are set here
    """
    pass