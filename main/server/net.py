'''
Created on 04.03.2014

@author: Solonarv
'''

from threading import Thread
from model.player import Player
import states

class ThreadListenForPlayers(Thread):
    def __init__(self, server, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.server=server
    
    def run(self):
        self.server.socket.listen(1)
        print "ThreadListenForPlayers started"
        while True:
            conn, addr=self.server.socket.accept()
            print "Incoming connection from %s:%i" % addr
            msg=conn.recv(1024)
            newplayer=ServerPlayer(msg, conn, addr, self.server)
            currplayers=','.join(["%s|%s" % (p.name,p.texpackname) for p in self.server.players])
            if not isinstance(self.server.state,states.StateJoining):
                conn.sendall("NAK:wrong-server-state")
                conn.close()
            elif len(self.server.players)>=self.server.maxplayers:
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
                self.server.state.addPlayer(newplayer)
                

class ServerPlayer(Player):
    def __init__(self, msg, conn, addr, server):
        name, texpack=msg.split(':',1) # Hello message expected in Name:texpack format
        Player.__init__(self, name, texpack)
        self.server=server
        self.conn=conn
        self.addr=addr