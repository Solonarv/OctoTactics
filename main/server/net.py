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