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


    def __init__(self, sock, sep=";\n", timeout=.2, recvbuf=4096):
        self.socket=sock
        self.timeout=timeout
        sock.settimeout(timeout)
        self.sep=sep
        self.recvbuf=4096
        self.queue=""
    
    def recv(self):
            while True: # Receive as much data as possible
                try:
                    self.queue+=self.socket.recv(self.recvbuf)
                    if self.sep in self.queue:
                        break
                except socket.error:  # Exit loop on EoF
                    break
            if self.sep in self.queue:
                x, xs=self.queue.split(self.sep, 1)
                self.queue=xs
                return x
            else:
                return ""
    
    def pushback(self, msg):
        """
        Shove a non-processed message back into the output end of the queue
        """
        self.queue="%s%s%s" % (msg, self.sep, self.queue)
    
    def send(self, msg):
        self.socket.setblocking(True)
        ret=self.socket.sendall(msg)
        self.socket.settimeout(self.timeout)
        return ret