'''
Created on 04.03.2014

@author: Solonarv
'''

from socket import error as SocketError
import socket

from model.board import Board, RA_MAX_ENERGY
from net import NullPlayer
from net import ServerPlayer


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
        pass # TODO use Twisted
        
    def addPlayer(self, player):
        # TODO use Twisted
        self.server.broadcast("INFO:player-joined:%s:%s" % (player.name, player.texpackname))
        self.server.players+=[player]
        if self.server.owner not in self.server.players:
            self.server.owner=self.server.players[1] # self.server.players[0] is RA, the null owner.
            if self.server.owner not in self.server.settings.ops:
                self.server.settings.ops+=[self.server.owner]
        print "Added player: %s" % player.name
        player.send(self.server.settings.encode())
        if len(self.server.players)==2 and player not in self.server.settings.ops:
            self.server.settings.ops+=[player]
        if len(self.server.players)>self.server.maxplayers:
            self.server.setstate(StatePregameLobby)
            return True
        return False

class StatePregameLobby(State):
    """Allow server owner (first player to join) to change game settings,
    allow players to change appearance."""
    def __init__(self, prevstate):
        State.__init__(self,prevstate.server)
        self.ready=set()
    
    def run(self):
        # TODO use Twisted
        pass
    
    def runcommand(self, player, cmd):
        # TODO use Twisted/DCProtocol
        pass
            
                

class StateInitializingGame(State):
    """Initialize game board before starting the game. Simple daemon/worker state.
    Once done, transition to StateIngame."""
    def __init__(self, prevstate):
        State.__init__(self, prevstate.server)
        self.board=None
    
    def run(self):
        self.board=Board(self.server.settings.boardw,self.server.settings.boardh, self.server.boardw, self.server.nullplayer)
        for (pname, x, y) in self.server.settings.starts:
            player=self.server.playerbyname(pname)
            if player!=None: self.board.cells[x, y].owner=player
        self.server.setstate(StateRunning)

class StateRunning(State):
    def __init__(self, prevstate):
        State.__init__(self, prevstate.server)
        self.board=prevstate.board
        self.ready={self.server.nullplayer}
        self._allplayers=frozenset(self.server.players)
        self.msgqueue={p.name:"" for p in self.server.players}
        self.cellcounts=self.board.countcells()
    
    def run(self):
        # TODO use Twisted
        pass
    
    def process(self, player, cmd):
        # TODO use Twisted
        pass
    
    def gameended(self):
        scores=self.board.countcells()
        ended=True
        for pn,cc in self.cellcounts.iteritems():
            if cc>0:
                ended=False
                self.cellcounts[pn]=scores[pn]
                if scores[pn]==0: pass # TODO use Twisted
        return ended
    
    def tick(self):
        self.board.tick()
        self.ready={self.server.nullplayer}
        # TODO use Twisted
        # self.server.broadcast("BOARD:"+self.board.encode())

class StatePostgame(State):
    """Postgame state. This state sends score & victory information to all players and lets them chat."""
    def __init__(self, prevstate):
        State.__init__(self, prevstate.server)
    
    def run(self):
        # Foo bar
        self.server.setstate(StateStopping)

class StateStopping(State):
    """Stop the game. This state is responsible for properly cleaning up and releasing resources. Once done, exit."""
    def __init__(self, prevstate):
        State.__init__(self, prevstate.server)
    
    def run(self):
        self.server.broadcast("ERR:server-stopping")
        for p in self.server.players:
            p.conn.shutdown(socket.SHUT_RDWR)
            p.conn.close()
        self.server.socket.close()
        
        exit()