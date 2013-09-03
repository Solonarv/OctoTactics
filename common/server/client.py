'''
Created on 19.08.2013

@author: Solonarv
'''

class ClientConnection(object):
    """
    Used server-side to represent a connection to a client
    """
    
    def __init__(self, stream):
        self.stream = stream
        stream.setblocking(False)
        