'''
Created on 31.07.2013

@author: Solonarv
'''
from server.server import Server
from server.dedicated.network.listen import ThreadNetworkListener
from threading import Lock

class ServerMP(Server):
    def __init__(self, port = 59786):
        super().__init__()
        self.connected_clients=[]
        self.clientlist_lock=Lock()
        self.network_listener = ThreadNetworkListener(self, port)
    def add_client(self, conn):
        with self.clientlist_lock:
            self.connected_clients.append(conn)