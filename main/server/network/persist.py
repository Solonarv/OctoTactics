'''
Created on 05.10.2013

@author: Solonarv
'''

from struct import Struct
from hashlib import md5
from server.network.events import ClientJoinedEvent

class ClientList:
    """
    Holds a list of all clients a server is connected to, as well
    as some methods to interact with that set of clients.
    """
    def __init__(self, server):
        self.clients = []
        self.server = server
    
    def addclient(self, tcp_stream, addr):
        client = ClientRepr(tcp_stream, addr)
        self.clients.append(client)
        self.server.EVENT_BUS.post(ClientJoinedEvent(self.server, client))
    
    def broadcast(self, msg):
        for cl in self.clients: cl.sendmsg(msg)

class ClientRepr:
    """
    Holds data about a specific client as connected to a server.
    """
    
    struct_ClientHello = Struct('>?32s')
    # Is the client an AI?
    # Client's self.given name
    
    nextsalt = 0
    
    def __init__(self, tcp_stream, addr):
        self.stream = tcp_stream
        self.address = addr
        self.handlefirst()
        self.stream.setblocking(False)
    
    def handlefirst(self):
        data = self.stream.read()
        ai, name = self.struct_ClientHello.unpack(data)
        self.isAI = ai
        self.clientname = str(name, encoding = "utf8").strip("\x00")
        # Compute a unique ID for the client based on the name id gave itself and a counter
        self.cluid = int.from_bytes((md5().update(name + self.nextsalt.to_bytes(4, 'big')).digest())[:8], 'big')
        self.nextsalt = (self.nextsalt * self.nextsalt + 23) & 0xFfffFfff
    
    def sendmsg(self, msg):
        self.stream.write(msg)