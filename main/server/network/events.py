'''
Created on 06.10.2013

@author: Solonarv
'''
from util.events import Event

class ServerEvent(Event):
    def __init__(self, server):
        self.server = server

class ClientJoinedEvent(ServerEvent):
    def __init__(self, server, client):
        super().__init__(server)
        self.client = client