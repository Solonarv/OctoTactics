'''
Created on 04.03.2014

@author: Solonarv
'''

from net import ServerPlayer
from util import GameSettings
from socket import error as SocketError


class State(object):
    """State base class"""
    def __init__(self, server):
        self.server=server
        print "Entering state: %s" % self.__class__
    def stop(self): pass
    def kill(self): pass

class StateJoining(State):
    """Wait for players to join, handling incoming TCP connections.
    Once maximum number of players is reached, transition to StatePregameLobby."""
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
            conn.setblocking(False)
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
            self.server.owner=self.server.owner[0]
        print "Added player: %s" % player.name
        player.conn.sendall(self.server.settings.encode())
        if len(self.server.players)==1:
            self.server.settings.ops+=[player]
        if len(self.server.players)>=self.server.maxplayers:
            self.server.setstate(StatePregameLobby)

class StatePregameLobby(State):
    """Allow server owner (first player to join) to change game settings,
    allow players to change appearance."""
    def __init__(self, prevstate):
        State.__init__(self,prevstate.server)
        self.msgqueue={p.name:"" for p in self.server.players}
    
    def run(self):
        if self.waitForReady():
            self.server.setstate(StateInitializingGame)
    
    def waitForReady(self):
        while True:
            for player in self.server.players:
                msginc=""
                while True: # Receive as much data as possible form the player
                    try:
                        msginc+=player.conn.recv(4096) 
                    except SocketError: break # Exit loop on EoF
                self.msgqueue[player.name]+=msginc # Add received data to player's message queue
                msgs=self.msgqueue[player.name].split(';')
                self.msgqueue[player.name]=msgs[-1] # message piece after last ; is what's left over and is stored for next iteration
                msgs=msgs[:-1]
                for cmd in msgs:
                    self.runcommand(player, cmd)
    
    def runcommand(self, player, cmd):
        if cmd.startswith("settexpack:"):
            texpack=cmd.split(":")[1]
            if any([p.texpackname==texpack for p in self.server.players]):
                player.conn.sendall("NAK:texpack-in-use;")
            else:
                player.changetex(texpack)
        elif cmd.startwith("setting:"):
            if player.name in self.server.settings.ops:
                if self.server.settings.setoption(*cmd.split(":")[1:2]):
                    player.conn.sendall("ACK:option-set;")
                else:
                    player.conn.sendall("NAK:option-not-set;")
            else:
                player.conn.sendall("NAK:option-not-set:no-rights;")
                

class StateInitializingGame(State):
    """Initialize game board before starting the game. Simple daemon/worker state.
    Once done, transition to StateIngame."""
    def __init__(self, prevstate):
        State.__init__(self, prevstate.server)
    
    def run(self): pass