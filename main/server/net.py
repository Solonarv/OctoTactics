'''
Created on 04.03.2014

@author: Solonarv
'''

from threading import Thread
from model.player import Player
import states

class ServerPlayer(Player):
    def __init__(self, msg, conn, addr, server):
        name, texpack=msg.split(':',1) # Hello message expected in Name:texpack format
        Player.__init__(self, name, texpack)
        self.server=server
        self.conn=conn
        self.addr=addr
    
    def send(self, msg):
        self.conn.sendall(msg+"\n")
        print "[NET] Sent to %s: %s" % (self.name, msg)
    
    def recv(self,buf=4096):
        rc=self.conn.recv(buf)
        print "[NET] Recv from %s: %s" % (self.name, rc)
        return rc

class NullPlayer(ServerPlayer):
    def __init__(self, server):
        ServerPlayer.__init__(self, name + "RA:<>", None, None, server)
    
    def send(self, msg): pass
    def recv(self, buf=4096): return ""