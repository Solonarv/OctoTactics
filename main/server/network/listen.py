'''
Created on 31.07.2013

@author: Solonarv
'''

import socketserver
from threading import Thread
from util.events import Event

class ThreadNetworkListener(Thread):
    def __init__(self, gameserver, port):
        super().__init__()
        self.tcpserver = None
        self.gameserver = gameserver
        self.port=port
    
    def run(self):
        if self.tcpserver == None:
            self.tcpserver=socketserver.TCPServer(('127.0.0.1', self.port), ServerConnectRequestHandler)
            self.tcpserver.parent_thread = self
        self.tcpserver.serve_forever()

class ServerConnectRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.server.parent_thread.gameserver.clients.add_client(self.request)