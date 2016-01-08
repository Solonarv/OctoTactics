'''
Created on 04.03.2014

@author: Solonarv
'''

from threading import Lock
from twisted.internet import protocol as twistedprotocol

from model import board
from network import protocol
from net import ServerPlayer,NullPlayer
import states
from sutil import GameSettings


class Server(twistedprotocol.Factory):
    def __init__(self, maxplayers):
        self.nullplayer=NullPlayer(self)
        self.players={self.nullplayer.id: self.nullplayer}
        self.owner=None
        self.maxplayers=maxplayers
        
        self.settings=GameSettings()
        
        self.statetype=states.StateJoining; self.state=self.statetype(self)
        self.stateLock=Lock()
        self.netmsghandler=OctoDCPMessageHandlerServerside()
    
    def startgame(self):
        self.board=board.Board()
    
    def setstate(self, stateType):
        """
        Change state from self.statetype to stateType.
        Thread safe, uses self.stateLock.
        """
        self.stateLock.acquire()
        
        self.statetype=stateType
        self.state.stop()
        newstate=self.stateType(self.state)
        self.state.kill()
        self.state=newstate
        
        self.stateLock.release()
    
    def playerbyname(self, pname):
        for p in (pname and self.players.values()): # Woo lazy eval!
            if p.name==pname: return p
        return None
    
    def buildProtocol(self, addr):
        return OctoProtocolServerside(self, self.netmsghandler)

class OctoProtocolServerside(protocol.DelegatingChannelProtocol):
    
    def connectionMade(self):
        self.player=ServerPlayer(self, hash(self))
        self.factory.players.add(self.player)
        for pl in self.factory.players.values():
            pl.sendLine("net/players/joined:%s" % self.player.id)
    
    def connectionLost(self, reason):
        self.factory.players.remove(self.player)
        for pl in self.factory.players.values():
            pl.sendLine("net/players/left:%s" % self.player.id)

class OctoDCPMessageHandlerServerside(protocol.DCMessageHandlerBase):
    def __init__(self, server, *args, **kwargs):
        protocol.DCMessageHandlerBase.__init__(self, *args, **kwargs)
        self.server=server
        
    def handle(self, protocol, chan, msg):
        if chan:
            if chan[0]=="chat": self.handleChat(protocol, chan[1:], msg)
        else: return
    
    def handleChat(self, protocol, chan, msg):
        if chan:
            if chan[0]=="tell" and len(chan)>=2 and chan[1]:
                try:
                    recvid=int(chan[1])
                    player=self.server.players[recvid]
                    player.sendLine("chat/tell/in/%i:%s" % (protocol.player.id, msg)) # Send the actual tell
                    protocol.sendLine("chat/tell/out/ok/%i:%s" % (recvid, msg)) # Success message
                except ValueError, KeyError:
                    print "Error in net handler: chat/tell/%s : invalid tell target id %s" % (chan[1], chan[1])
                    protocol.sendLine("chat/tell/out/fail/%s:%s" % (chan[1], msg))