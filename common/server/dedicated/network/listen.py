'''
Created on 31.07.2013

@author: Solonarv
'''

import socketserver
from threading import Thread
from server.client import ClientConnection

class ThreadNetworkListener(Thread):
    def __init__(self, gameserver, port):
        super().__init__()
        self.tcpserver = None
        self.gameserver = gameserver
        self.port=port
    
    def run(self):
        if self.tcpserver == None:
            self.tcpserver=socketserver.TCPServer(('127.0.0.1', self.port), ServerConnectRequestHandler(self))
            self.tcpserver.parent_thread = self
        self.tcpserver.serve_forever()

def ServerConnectRequestHandler(thread):
    class result(socketserver.BaseRequestHandler):
        def handle(self):
            thread.gameserver.add_client(ClientConnection(self.request))
    return result
        