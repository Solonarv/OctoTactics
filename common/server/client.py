'''
Created on 19.08.2013

@author: Solonarv
'''

class ClientConnection(object):
    
    def __init__(self, stream):
        self.stream = stream
        stream.setblocking(False)
    def _message(self, msg):
        self.stream.send(msg)
    def sendcellinfo(self, cell):
        msg=bytearray()
        