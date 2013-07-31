'''
Created on 31.07.2013

@author: Solonarv
'''
from server.Server import Server
from threading import Thread
from server.dedicated.network.listen import server_listen_network

class ServerMP(Server):


    def __init__(self):
        super().__init__()
        self.connected_clients=[]
        self.network_listener = ThreadNetworkListener()
        