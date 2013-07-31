'''
Created on 31.07.2013

@author: Solonarv
'''

import socketserver
from threading import Thread

class ThreadNetworkListener(Thread):
    def __init__(self, port):
        super().__init__()
        self.server=None
        self.port=port
    
    def run(self):
        if self.server == None:
            self.server=socketserver.TCPServer(('127.0.0.1', self.port), ServerConnectRequestHandler)
        self.server.serve_forever()

class ServerConnectRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pass
        