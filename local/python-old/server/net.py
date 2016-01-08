'''
Created on Jun 1, 2014

@author: solonarv
'''
from model.player import Player

class ServerPlayer(Player):
    
    def __init__(self, conn, hsh):
        Player.__init__(self, "", "")
        self.conn=conn
    
    def sendLine(self,line):
        return self.conn.sendLine(line)

class NullPlayer(ServerPlayer):
    
    def __init__(self, server):
        ServerPlayer.__init__(self, None, -1)
    
    def sendLine(self, line):
        pass