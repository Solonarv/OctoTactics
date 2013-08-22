'''
Created on 22.08.2013

@author: Solonarv
'''
from server.model.Cell import Cell

side=object()
side.serverSide=True
side.clientSide=True

try:
    import server.dedicated.ServerMP as foo
    del foo
except ImportError:
    side.serverSide=False

try:
    import client.model as bar
    del bar
except ImportError:
    side.clientSide=False

from abc import ABCMeta, abstractmethod, abstractclassmethod
import pickle

class Packet(object, metaclass=ABCMeta):
    def __init__(self):
        pass
    
    def encodeval(self):
        return pickle.dumps(self.val)
    @abstractmethod
    def encode(self):
        pass
    
    @classmethod
    def decodeval(cls, data):
        return pickle.loads(data)
    @abstractclassmethod
    def decode(cls, data):
        pass

class ServerToClient(Packet):
    _allowed_server_types=()
    def __new__(cls, data, *args, **kwargs):
        if((side.serverSide and isinstance(data, cls._allowed_server_types))
           or (side.clientSide and isinstance(data, (bytes,bytearray)))):
            return Packet.__new__(cls, data, *args, **kwargs)
        

class Packet001Cell(ServerToClient, Packet):
    _allowed_server_types = (Cell,)
    @abstractmethod
    def encode(self):
        Packet.encode(self)