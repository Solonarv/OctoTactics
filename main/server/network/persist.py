'''
Created on 05.10.2013

@author: Solonarv
'''

from struct import Struct

class ClientList:
    """
    Holds a list of all clients a server is connected to, as well
    as some methods to interact with that set of clients.
    """
    def __init__(self):
        self.clients = []
    
    def addclient(self, tcp_stream, addr):
        self.clients.append(ClientRepr(tcp_stream, addr))

class ClientRepr:
    """
    Holds data about a specific client as connected to a server.
    """
    
    struct_ClientHello = Struct('>?32s')
    
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
    
    def sendmsg(self, msg):
        pass