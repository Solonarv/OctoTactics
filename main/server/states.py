'''
Created on 04.03.2014

@author: Solonarv
'''

from net import ServerPlayer
from util import GameSettings


class State(object):
    def __init__(self, server):
        self.server=server
        print "Entering state: %s" % self.__class__
    def stop(self): pass
    def kill(self): pass

class StateJoining(State):
    def __init__(self, server):
        State.__init__(self, server)
    
    def run(self):
        self.server.socket.listen(1)
        print "Listening for incoming connections"
        while True:
            conn, addr=self.server.socket.accept()
            print "Incoming connection from %s:%i" % addr
            msg=conn.recv(1024)
            newplayer=ServerPlayer(msg, conn, addr, self.server)
            currplayers=','.join(["%s|%s" % (p.name,p.texpackname) for p in self.server.players])
            if len(self.server.players)>=self.server.maxplayers:
                conn.sendall("NAK:server-full")
                conn.close()
            elif [p for p in self.server.players if p.name==newplayer.name]:
                conn.sendall("NAK:duplicate-playername;players:"+currplayers)
                conn.close()
            elif [p for p in self.server.players if p.texpackname==newplayer.texpackname]:
                conn.sendall("NAK:duplicate-texpack;players:"+currplayers)
                conn.close()
            else:
                conn.sendall("ACK:joined;players:"+currplayers+"\n")
                self.addPlayer(newplayer)
    
    def addPlayer(self, player):
        self.server.players+=[player]
        if self.server.owner not in self.server.players:
            self.server.owner=player
        print "Added player: %s" % player.name
        player.conn.sendall(self.server.settings.encode())
        if len(self.server.players)==1:
            self.server.settings.ops+=[player]
        if len(self.server.players)>=self.server.maxplayers:
            self.server.setstate(StatePregameLobby)

class StatePregameLobby(State):
    def __init__(self, prevstate):
        State.__init__(self,prevstate.server)
    
    def run(self):
        self.running=True
        while self.running:
            msg=self.server.owner.conn.recv(4096).split('\n')
            for line in msg:
                for setting in line.split(";"):
                    option, args=setting.split(":")
                    self.server.settings.setoption(option, args)