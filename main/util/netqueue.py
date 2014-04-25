'''
Created on Apr 25, 2014

@author: solonarv
'''
import socket


class NetQueue(object):
    '''
    Abstraction over the socket lib that splits the
    stream on a separator and enqueues the pieces.
    
    Call recv() to get the next piece.
    '''


    def __init__(self, socket, sep=";\n", blocking=True, recvbuf=4096):
        self.socket=socket
        self.blocking=blocking
        socket.setblocking(blocking)
        self.sep=sep
        self.recvbuf=4096
        self.queue=[]
        self.leftovers=""
    
    def recv(self):
        if self.queue:
            return self.queue.pop(0)
        else:
            if self.blocking:
                while not self.leftovers.count(self.sep): # receive data into self.leftovers until it contains self.sep
                    self.leftovers+=self.recv(self.recvbuf)
            else:
                receiving=True
                while receiving: # Receive as much data as possible
                    try:
                        self.leftovers+=self.socket.recv()
                    except socket.error: receiving=False # Exit loop on EoF
            msgs=self.leftovers.split(self.sep)
            self.leftovers=msgs[-1]
            msgs=msgs[:-1]
            msgs=filter(None, msgs) # discard empty messages
            self.queue=msgs
    
    def send(self, msg):
        return self.socket.sendall(msg)