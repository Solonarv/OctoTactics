'''
Created on 16.10.2013

@author: Solonarv
'''

from struct import Struct
from util.structhelper import ulonglong

class Packet:
    tpid = 0
    
    def encode(self):
        return bytes((self.tpid,)) + self._encode()
    
    def _encode(self): return bytes()

class ClientJoinedPacket(Packet):
    tpid=1
    
    struct_ClientJoinedBroadcast = Struct(">?Q32s")
    # Is it an AI?
    # The client's UID
    # The client's name (32char string)
    
    def __init__(self, client):
        self.client = client
    
    def _encode(self):
        return self.struct_ClientJoinedBroadcast.pack(self.client.isAI, self.client.cluid, self.client.clientname)

class ClientReadyPacket(Packet):
    tpid=2
    
    def __init__(self, client):
        self.client = client
    
    def _encode(self):
        return ulonglong.pack(self.client.cluid)