'''
Created on 04.03.2014

@author: Solonarv
'''

from socket import error as SocketError
import socket

from model.board import Board, RA_MAX_ENERGY
from net import NullPlayer
from net import ServerPlayer
from util import GameSettings


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
            newplayer=ServerPlayer(msg.strip("\n"), conn, addr, self.server)
            conn.setblocking(False)
            currplayers=','.join(["%s|%s" % (p.name,p.texpackname) for p in self.server.players])
            if len(self.server.players)>self.server.maxplayers:
                conn.sendall("NAK:server-full;\n")
                print "Server is full; it should not be in StateJoining anymore! This is a bug."
                conn.close()
            elif [p for p in self.server.players if p.name==newplayer.name]:
                conn.sendall("NAK:duplicate-playername;players:%s;\n" % currplayers)
                print "Player %s attempted to join with duplicate name, request denied." % p.name
                conn.close()
            elif [p for p in self.server.players if p.texpackname==newplayer.texpackname]:
                conn.sendall("NAK:duplicate-texpack;players:%s;\n" % currplayers)
                print "Player %s attempted to join with duplicate texture pack %s, request denied" % (p.name, p.texpackname)
                conn.close()
            else:
                conn.sendall("ACK:joined;players:"+currplayers+"\n")
                if self.addPlayer(newplayer): break
    
    def addPlayer(self, player):
        self.server.players+=[player]
        if self.server.owner not in self.server.players:
            self.server.owner=self.server.players[1] # self.server.players[0] is RA, the null owner.
            if self.server.owner not in self.server.settings.ops:
                self.server.settings.ops+=[self.server.owner]
        print "Added player: %s" % player.name
        player.conn.sendall(self.server.settings.encode())
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
        self.msgqueue={p.name:"" for p in self.server.players}
        self.ready=set()
    
    def run(self):
        for player in self.server.players:
            player.send("owner-name:%s" % self.server.owner.name)
        if self.waitForReady():
            self.server.setstate(StateInitializingGame)
        else:
            self.server.setstate(StateStopping)
    
    def waitForReady(self):
        while True:
            for player in [p for p in self.server.players if not isinstance(p, NullPlayer)]:
                msginc=""
                receiving=True
                while receiving: # Receive as much data as possible form the player
                    try:
                        msginc+=player.recv().strip("\n")
                    except SocketError: receiving=False # Exit loop on EoF
                self.msgqueue[player.name]+=msginc # Add received data to player's message queue
                msgs=self.msgqueue[player.name].split(';')
                self.msgqueue[player.name]=msgs[-1] # message piece after last ; is what's left over and is stored for next iteration
                msgs=msgs[:-1]
                for cmd in msgs:
                    if self.runcommand(player, cmd.strip('\n'))=="QUIT":
                        return False
            if self.ready.issuperset(self.server.players):
                return True
    
    def runcommand(self, player, cmd):
        print "Processing command from player %s: %s" % (player.name, cmd)
        if player in self.ready: pass
        elif cmd.startswith("settexpack:"):
            texpack=cmd.split(":")[1]
            if any([p.texpackname==texpack for p in self.server.players]):
                player.send("NAK:texpack-in-use")
            else:
                player.changetex(texpack)
                player.send("ACK:texpack-changed:%s" % texpack)
                self.server.broadcast("INFO:texpack-changed:%s:%s" % (player.name, texpack))
        elif cmd.startswith("setting:"):
            opt, args=cmd.split(":",2)[1:]
            if player in self.server.settings.ops:
                if self.server.settings.setoption(opt, args):
                    player.send("ACK:option-set:'%s:%s'\n" % (opt, args))
                    self.server.broadcast("INFO:options-changed:%s" % self.server.settings.encode())
                else:
                    player.send("NAK:option-not-set:unknown:'%s:%s'" % (opt, args))
            else:
                player.send("NAK:option-not-set:no-rights:'%s:%s'" % (opt, args))
        elif cmd=="ready":
            if self.server.settings.startsok():
                self.ready.add(player)
                player.send("ACK:ready-check")
                self.server.broadcast("INFO:player-ready:%s" % player.name)
            else:
                player.send("NAK:startless-players")
            
                

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
        while True:
            for player in [p for p in self.server.players if not isinstance(p, NullPlayer)]:
                msginc=""
                receiving=True
                while receiving: # Receive as much data as possible form the player
                    try:
                        msginc+=player.recv().strip("\n")
                    except SocketError: receiving=False # Exit loop on EoF
                self.msgqueue[player.name]+=msginc # Add received data to player's message queue
                msgs=self.msgqueue[player.name].split(';')
                self.msgqueue[player.name]=msgs[-1] # message piece after last ; is what's left over and is stored for next iteration
                msgs=msgs[:-1]
                for cmd in msgs:
                    self.process(player, cmd.strip('\n'))
                if self.ready==self._allplayers:
                    self.tick()
                if self.gameended():
                    self.server.setstate(StatePostgame)
    
    def process(self, player, cmd):
        if player in self.ready:
            player.send("NAK:locked-in")
            return
        if cmd.startswith("untarget:"):
            try:
                xf, yf, xt, yt=(int(x) for x in cmd.split(":",4)[1:])
            except ValueError:
                player.send("NAK:no-untarget:bad-coord-format")
                return
            try:
                fcell=self.board.cells[xf,yf]
                tcell=self.board.cells[xt,yt]
            except KeyError:
                player.send("NAK:no-untarget:coords-out-of-bounds")
                return
            if fcell.owner!=player:
                player.send("NAK:cell-not-owned")
                return
            try:
                fcell.targets.remove(tcell)
                player.send("ACK:cell-untargeted:%i,%i:%i,%i" % (xf,yf,xt,yt))
            except ValueError:
                player.send("ACK:already-done")
        elif cmd.startswith("target:"):
            try:
                xf, yf, xt, yt=(int(x) for x in cmd.split(":",4)[1:])
            except ValueError:
                player.send("NAK:no-target:bad-coord-format")
                return
            try:
                fcell=self.board.cells[xf,yf]
                tcell=self.board.cells[xt,yt]
            except KeyError:
                player.send("NAK:no-target:coords-out-of-bounds")
                return
            if fcell.owner!=player:
                player.send("NAK:cell-not-owned")
                return
            if tcell in fcell.targets:
                player.send("ACK:already-done")
                return
            if len(fcell.targets) > fcell.maxTargets:
                player.send("NAK:too-many-targets")
                return
            if (xf-xt)*(xf-xt)+(yf-yt)*(yf-yt) > fcell.rangeSq:
                player.send("NAK:out-of-range")
                return
            fcell.targets.append(tcell)
        elif cmd=="forfeit":
            if self.cellcounts[player.name]<=0:
                player.send("NAK:game-over")
                return
            self.cellcounts[player.name]=-1
            for cell in self.board.cells.values():
                if cell.owner==player:
                    cell.owner=self.server.nullowner
                    cell.targets=[]
                    cell.energy=max(cell.energy, RA_MAX_ENERGY)
            player.send("ACK:forfeited")
        elif cmd=="ready":
            self.ready.add(player)
    
    def gameended(self):
        scores=self.board.countcells()
        ended=True
        for pn,cc in self.cellcounts.iteritems():
            if cc>0:
                ended=False
                self.cellcounts[pn]=scores[pn]
                if scores[pn]==0: self.server.playerbyname(pn).send("INFO:lost-all-cells")
        return ended
    
    def tick(self):
        self.board.tick()
        self.ready={self.server.nullplayer}
        self.server.broadcast(self.board.encode())

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