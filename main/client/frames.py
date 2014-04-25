'''
Created on Apr 25, 2014

@author: solonarv
'''
from os import chdir
import socket

import Tkinter as tk
from render.render import TexPack
from network.netqueue import NetQueue

def decodeoptions(options):
    size, starts, ops=options.split("|")
    bw, bh=size.split("x")
    bw, bh=int(bw), int(bh)
    starts=[dat.split(":") for dat in starts.split(",")] if starts else []
    starts=[(pn, int(pos.split("x")[0]), int(pos.split("x")[1])) for (pn, pos) in starts] if starts else []
    ops=ops.split(",")
    return (bw, bh, starts, ops)

class FrameOT(tk.Frame):
    def __init__(self, title, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent=parent
        self.parent.title(title)
        self.pack(fill=tk.BOTH, expand=1)
    
    def mkWidgets(self): pass

class FrameConnect(FrameOT):
    def __init__(self, parent, *args, **kwargs):
        FrameOT.__init__(self, "OctoTactics: Connect", parent, *args, **kwargs)
        self.connected=False
    
    def mkWidgets(self):
        self.lbUsername=tk.Label(self, width=20, text="User name")
        self.lbUsername.grid(row=1, column=0)
        self.boxUsername=tk.Entry(self, width=20)
        self.boxUsername.grid(row=1, column=1)
        
        self.lbServerAddr=tk.Label(self, width=20, text="Server address")
        self.lbServerAddr.grid(row=2, column=0)
        self.boxServerAddr=tk.Entry(self, width=20)
        self.boxServerAddr.grid(row=2, column=1)
        
        self.lbTexPack=tk.Label(self, width=20, text="Texture pack")
        self.lbTexPack.grid(row=3, column=0)
        self.boxTexPack=tk.Entry(self, width=20)
        self.boxTexPack.grid(row=3, column=1)
        
        self.btnConnect=tk.Button(self, command=self.connect, width=10, text="Connect")
        self.btnConnect.grid(row=4, column=0)
        self.lbStatus=tk.Label(self, width=30, text="")
        self.lbStatus.grid(row=4, column=1)
        
        self.plist=tk.Listbox(self, state=tk.DISABLED, width=50, height=5)
        self.plist.grid(row=1, column=2, rowspan=3)
        self.lbPlist=tk.Label(self, text="Players:", width=10)
        self.lbPlist.grid(row=0, column=2, sticky=tk.W)
        self.plYScroll=tk.Scrollbar(self, orient=tk.VERTICAL, command=self.plist.yview())
        self.plYScroll.grid(row=1, column=3, rowspan=3, sticky=tk.N+tk.S)
        self.plist.config(yscrollcommand=self.plYScroll.set)
        
        self.bind_all("<KeyPress-Return>", self.connect)
        self.boxUsername.focus_set()
    
    def connect(self, e=None):
        """Attempt to connect to the server entered by the user."""
        print "Connect button/Enter key activated. Connected:" + str(self.connected)
        if self.connected: return # Don't attempt connection if there already is one, duh!
        # Check existence of texture pack
        if self.boxUsername.get()=="":
            self.setstatus("User name must not be empty")
            return
        if self.boxUsername.get().count(":"):
            self.setstatus("User name may not contain colons (:)")
            return
        elif not TexPack.istexpack(self.boxTexPack.get()):
            self.setstatus("Texture pack does not exist")
            return
        else:
            self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                addr=self.getAddr()
                self.socket.connect(addr)
                self.socket.setblocking(True)
                self.socket.sendall("%s:%s" % (self.boxUsername.get(), self.boxTexPack.get()))
                self.nq=NetQueue(self.socket)
                msg=self.nq.recv()
                if msg.startswith("NAK:"):
                    if msg=="NAK:server-full\n":
                        self.setstatus("Server is full")
                        return
                    elif msg.startswith("NAK:duplicate-playername;players:"):
                        self.setstatus("Name already in use")
                        self.showplayers([tuple(s.split("|")) for s in msg.split(";players:")[1].strip("\n").split(",")])
                    elif msg.startswith("NAK:duplicate-texpack;players:"):
                        self.setstatus("Texture pack already in use")
                        self.showplayers([tuple(s.split("|")) for s in msg.split(";players:")[1].strip("\n").split(",")])
                    else:
                        self.setstatus("Server refused connection")
                    return
                elif msg.startswith("ACK:"):
                    self.setstatus("Connected!")
                    self.showplayers([tuple(s.split("|")) for s in msg.split(";players:")[1].strip("\n").split(",")] + [(self.boxUsername.get(), self.boxTexPack.get())])
                    self.connected=True
                    self.btnConnect.config(state=tk.DISABLED)
                    self.boxServerAddr.config(state=tk.DISABLED, text=addr[0])
                    self.boxTexPack.config(state=tk.DISABLED)
                    self.boxUsername.config(state=tk.DISABLED)
                    self.recvsettings()
                    self.serverfill_timer()
            except ValueError:
                self.setstatus("Invalid server address")
                raise
                return
            except socket.error:
                self.setstatus("Internal socket error")
                return
    
    def showplayers(self, players):
        self.players=players
        self.plist.config(state=tk.NORMAL)
        self.plist.delete(0, tk.END)
        l=["%s: %s" % (name, tex) for name, tex in players]
        self.plist.insert(tk.END, *l)
        self.plist.config(state=tk.DISABLED)
    
    def recvsettings(self):
        settings_msg=self.nq.recv()
        self.gamesettings=decodeoptions(settings_msg)
    
    def getAddr(self):
        a=self.boxServerAddr.get()
        if a=="": return ("localhost",56239)
        if a.count(":")>1: raise ValueError
        try:
            h, p=a.split(":")
            return h, int(p) if p!="" else 56239
        except ValueError:
            if a.count(":"): raise
            return (a, 56239)
    
    def setstatus(self, status):
        return self.lbStatus.config(text=status)
    
    def serverfill_timer(self):
        msg=self.nq.recv()
        if msg.startswith("INFO:player-joined:"):
            print "Received player join info from server"
            name, tex=msg.split("player-joined:",1)[1].split(":",1)
            self.plist.insert(tk.END, "%s: %s" % (name, tex))
            self.players+=[(name, tex)]
            self.showplayers(self.players)
        elif msg.startswith("INFO:owner-name:"):
            print "Received server owner info, switching into Pregame Lobby"
            owner=msg.split("owner-name:",1)[1]
            self.serverowner=owner
            fr=FramePregameLobby(self.parent)
            fr.takeover(self)
            self.destroy()
            fr.mkWidgets()
            return
        self.after(50, self.serverfill_timer)

class FramePregameLobby(FrameOT):
    def __init__(self, parent, *args, **kwargs):
        FrameOT.__init__(self, "OctoTactics: Pre-game Lobby", parent, *args, **kwargs)
        self.readypls=set()
    
    def takeover(self, prev):
        self.players=prev.players
        self.serverowner=prev.serverowner
        self.nq=prev.nq
        self.gamesettings=prev.gamesettings
        self.username=prev.boxUsername.get()
        self.texpack=prev.boxTexPack.get()
    
    def mkWidgets(self): # I hate UI programming now.
        self.lbxPlayers=tk.Listbox(self, height=5)
        self.lbxPlayers.grid(row=1, column=0, columnspan=6, sticky=tk.W+tk.E)
        self.plYScroll=tk.Scrollbar(self, orient=tk.VERTICAL, command=self.lbxPlayers.yview)
        self.plYScroll.grid(row=1, column=6, sticky=tk.N+tk.S)
        self.lbxPlayers.config(yscrollcommand=self.plYScroll.set)
        self.lbPlayerList=tk.Label(self, text="Players")
        self.lbPlayerList.grid(row=0, column=0, sticky=tk.W)
        self.opDeopBtn=tk.Button(self, command=self.toggleOp, text="Op/Deop",
                                 state=tk.NORMAL if self.username==self.serverowner or self.username in self.gamesettings[3] else tk.DISABLED)
        self.opDeopBtn.grid(row=0, column=5, sticky=tk.E)
        
        self.lbBWidth=tk.Label(self, text="Width")
        self.lbBWidth.grid(row=2, column=0, sticky=tk.E)
        self.sbxWidth=tk.Spinbox(self, from_=2, to=99, textvariable=self.gamesettings[0])
        self.sbxWidth.grid(row=2, column=1, sticky=tk.E+tk.W)
        self.lbBHeight=tk.Label(self, text="Height")
        self.lbBHeight.grid(row=2, column=2, sticky=tk.E)
        self.sbxHeight=tk.Spinbox(self, from_=2, to=99, textvariable=self.gamesettings[1])
        self.sbxHeight.grid(row=2, column=3, sticky=tk.E+tk.W)
        self.btnCommitWH=tk.Button(self, text="Save")
        self.btnCommitWH.grid(row=2, column=4, sticky=tk.E+tk.W)
        
        self.lbChangeTx=tk.Label(self, text="Change texture pack")
        self.lbChangeTx.grid(row=3, column=1, sticky=tk.E)
        self.boxChangeTx=tk.Entry(self, text=self.texpack)
        self.boxChangeTx.grid(row=3, column=3, sticky=tk.E+tk.W)
        self.btnChangeTx=tk.Button(self, text="Change", command=self.changetex)
        self.btnChangeTx.grid(row=3, column=4, sticky=tk.E)
        
        self.lbxStarts=tk.Listbox(self, height=5)
        self.lbxStarts.grid(row=5, column=0, columnspan=6, sticky=tk.W+tk.E)
        self.stYScroll=tk.Scrollbar(self, orient=tk.VERTICAL, command=self.lbxStarts.yview)
        self.stYScroll.grid(row=5, column=6, sticky=tk.N+tk.S)
        self.lbxStarts.config(yscrollcommand=self.stYScroll.set)
        self.lbStartList=tk.Label(self, text="Your starts")
        self.lbStartList.grid(row=4, column=0, sticky=tk.W)
        
        self.lbStartX=tk.Label(self, text="X")
        self.lbStartX.grid(row=6, column=0, sticky=tk.E)
        self.sbxStartX=tk.Spinbox(self, from_=0, to=self.gamesettings[0])
        self.sbxStartX.grid(row=6, column=1, sticky=tk.E+tk.W)
        self.lbStartY=tk.Label(self, text="Y")
        self.lbStartY.grid(row=6, column=2, sticky=tk.E)
        self.sbxStartY=tk.Spinbox(self, from_=0, to=self.gamesettings[1])
        self.sbxStartY.grid(row=6, column=3, sticky=tk.E+tk.W)
        
        self.btnAddStart=tk.Button(self, text="Add", command=self.addstart,
                                   state=tk.NORMAL if self.username==self.serverowner or self.username in self.gamesettings[3] else tk.DISABLED)
        self.btnAddStart.grid(row=6, column=4)
        self.btnRmvStart=tk.Button(self, text="Remove", command=self.removestart,
                                   state=tk.NORMAL if self.username==self.serverowner or self.username in self.gamesettings[3] else tk.DISABLED)
        self.btnRmvStart.grid(row=6,column=5)
        
        self.btnReady=tk.Button(self, text="READY", command=self.lockin)
        self.btnReady.grid(row=2, column=5, columnspan=2)
        
        self.lbStatus=tk.Label(self, text="")
        self.lbStatus.grid(row=7, column=0, columnspan=7, sticky=tk.E+tk.W)
        
        self.redrawplayerlist()
        self.redrawstartlist()
        self.ready_timer()
        
        self.lbxPlayers.bind("<ButtonRelease-1>", self.redrawstartlist)
        self.lbxStarts.bind("<ButtonRelease-1>", self.onstartselect)
        self.bind_all("<KeyPress-Return>", self.lockin)
    
    def redrawplayerlist(self):
        sel=self.lbxPlayers.curselection()
        sel=int(sel[0]) if sel else 0
        self.lbxPlayers.delete(0, tk.END)
        self.lbxPlayers.insert(0, *["%s: %s%s" % (pn, tx, " (owner)" if pn==self.serverowner else " (op)" if pn in self.gamesettings[3] else "") for (pn, tx) in self.players])
        self.lbxPlayers.activate(sel)
    
    def redrawstartlist(self, e=None):
        self.lbxStarts.delete(0, tk.END)
        curname=self.getselectedplayer()
        self.lbxStarts.insert(0, *["%i, %i: %s" % (x, y, "square" if (x+y)%2 else "octogon") for (pname, x, y) in self.gamesettings[2] if pname==curname])
    
    def onstartselect(self, e=None):
        curname=self.getselectedplayer()
        startnb=int(self.lbxStarts.curselection()[0])
        x, y=[(x, y) for (p, x, y) in self.gamesettings[2] if p==curname][startnb]
    
    def toggleOp(self):
        print "Toggle op button pressed"
        if self.username==self.serverowner or self.username in self.gamesettings[3]:
            tar=self.getselectedplayer()
            if tar==self.serverowner:
                self.setstatus("Can't deop the server owner!")
                return
            elif tar in self.gamesettings[3]:
                self.nq.send("setting:deop:"+tar)
                resp=self.nq.recv()
                if resp.startswith("NAK:option-not-set:"):
                    if resp.startswith("NAK:option-not-set:no-rights:"):
                        self.setstatus("You do not have the right to do that")
                    else:
                        self.setstatus("Unknown server error")
                    return
                elif resp.startswith("ACK:"):
                    self.setstatus("Removed op status from "+tar)
                else:
                    self.nq.pushback(resp)
            else:
                self.nq.send("setting:makeop:"+tar)
                resp=self.nq.recv()
                if resp.startswith("NAK:option-not-set:"):
                    if resp.startswith("NAK:option-not-set:no-rights:"):
                        self.setstatus("You do not have the right to do that")
                    else:
                        self.setstatus("Unknown server error")
                    return
                elif resp.startswith("ACK:"):
                    self.setstatus("Granted op status to "+tar)
                else:
                    self.nq.pushback(resp)
        else:
            self.setstatus("You do not have the rights to do that")
    
    def changetex(self):
        print "Change texpack button pressed"
        newtex=self.boxChangeTx.get()
        if not TexPack.istexpack(newtex):
            self.setstatus("Texture pack does not exist")
            return
        for pn, tx in self.players:
            if pn!=self.username and tx==newtex:
                self.setstatus("Texture pack already used by " + pn)
        self.nq.socket.sendall("settexpack:"+newtex)
        resp=self.nq.recv()
        if resp.startswith("NAK:"):
            if resp.startswith("NAK:texpack-in-use"):
                self.setstatus("Texture pack already in use")
            else:
                self.setstatus("Unknown server error")
        elif resp.startswith("ACK:"):
            self.setstatus("Texture pack successfully changed");
        else:
            self.nq.pushback(resp)
    
    def addstart(self, e=None):
        print "Add start button pressed"
        if self.username==self.serverowner or self.username in self.gamesettings[3]:
            tar=self.getselectedplayer()
            try:
                tx=int(self.sbxStartX.get())
                ty=int(self.sbxStartY.get())
            except ValueError:
                self.setstatus("Coordinates must be integers")
                return
            if tx<0 or tx>=self.gamesettings[0] or ty<0 or ty>=self.gamesettings[1]:
                self.setstatus("Start position must not be outside of board")
                return
            for pn, x, y in self.gamesettings[2]:
                if (x, y)==(tx, ty):
                    self.setstatus("Start position already take by " + pn)
                    return
            self.nq.send("setting:addstart:%s,%i,%i" % (tar, tx, ty))
            resp=self.nq.recv()
            if resp.startswith("NAK:option-not-set:"):
                if resp.startswith("NAK:option-not-set:no-rights:"):
                    self.setstatus("You do not have the right to do that")
                else:
                    self.setstatus("Unknown server error")
                    return
            elif resp.startswith("ACK:"):
                self.setstatus("Gave start position %i, %i to %s" % (tx, ty, tar))
            else:
                self.nq.pushback(resp)
        else:
            self.setstatus("You do not have the rights to do that")
    
    def removestart(self, e=None):
        print "Remove start button pressed"
        if self.username==self.serverowner or self.username in self.gamesettings[3]:
            tar=self.getselectedplayer()
            try:
                tx=int(self.sbxStartX.get())
                ty=int(self.sbxStartY.get())
            except ValueError:
                self.setstatus("Coordinates must be integers")
                return
            if tx<0 or tx>=self.gamesettings[0] or ty<0 or ty>=self.gamesettings[1]:
                self.setstatus("Start position must not be outside of board")
                return
            if (tar, tx, ty) not in self.gamesettings[2]:
                self.setstatus("Start position is not assigned to selected player")
            self.nq.send("setting:removestartstart:%s,%i,%i" % (tar, tx, ty))
            resp=self.nq.recv()
            if resp.startswith("NAK:option-not-set:"):
                if resp.startswith("NAK:option-not-set:no-rights:"):
                    self.setstatus("You do not have the right to do that")
                else:
                    self.setstatus("Unknown server error")
                    return
            elif resp.startswith("ACK:"):
                self.setstatus("Took start position %i, %i from %s" % (tx, ty, tar))
            else:
                self.nq.pushback(resp)
        else:
            self.setstatus("You do not have the rights to do that")
    
    def lockin(self, e=None):
        print "READY button pressed"
        startless=set([pn for pn, _ in self.players])
        for pn, _, _ in self.gamesettings[2]:
            startless.remove(pn)
        if startless:
            self.setstatus("Not all players have 1+ starting position")
            return
        self.nq.send("ready")
        self.btnAddStart.config(state=tk.DISABLED)
        self.btnChangeTx.config(state=tk.DISABLED)
        self.btnReady.config(state=tk.DISABLED)
        self.btnRmvStart.config(state=tk.DISABLED)
        resp=self.nq.recv()
        if resp.startswith("ACK:"):
            self.setstatus("Locked in options.")
        elif resp.startswith("NAK:"):
            if resp.startswith("NAK:startless-players"):
                self.setstatus("Not all players have 1+ starting position")
            else:
                self.setstatus("Unknown server error")
        else:
            self.nq.pushback(resp)
    
    def getselectedplayer(self):
        sel=self.lbxPlayers.curselection()
        return self.players[int(sel[0]) if sel else 0][0]
    
    def setstatus(self, status):
        return self.lbStatus.config(text=status)
    
    def ready_timer(self):
        msg=self.nq.recv()
        if msg.startswith("INFO:"):
            if msg.startswith("INFO:texpack-changed"):
                player, tex=msg.split(":", 3)[2:4]
                print player, tex
                self.players=[(pn, tx) if pn!=player else (player, tex) for pn, tx in self.players]
                print self.players
                if player==self.username:
                    self.texpack=tex
                    self.boxChangeTx.config(text=tex)
                self.redrawplayerlist()
            elif msg.startswith("INFO:options-changed:"):
                newopts=msg.split(":options-changed:",1)[1]
                self.gamesettings=decodeoptions(newopts)
                self.redrawplayerlist()
                self.redrawstartlist()
            elif msg.startswith("INFO:player-ready:"):
                rdy=msg.split(":player-ready:")[1]
                self.readypls.add(rdy)
        elif msg.startswith("BOARD:"):
            self.boarddata=msg[6:]
            # TODO do stuff
            return
        elif msg!="":
            self.nq.pushback(msg)
        self.after(50, self.ready_timer)
            

if __name__=="__main__":
    chdir("..")
    root=tk.Tk()
    fr=FrameConnect(root)
    fr.mkWidgets()
    root.mainloop()