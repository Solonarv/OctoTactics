'''
Created on 06.10.2013

@author: Solonarv
'''
from util.events import Event

class ServerEvent(Event):
    def __init__(self, server):
        self.server = server

class ClientEvent(ServerEvent):
    def __init__(self, server, client):
        super().__init__(server)
        self.client = client

class ClientJoinedEvent(ClientEvent): pass

class ClientReadyEvent(ClientEvent): pass