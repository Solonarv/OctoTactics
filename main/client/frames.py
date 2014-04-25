'''
Created on Apr 25, 2014

@author: solonarv
'''
from os import chdir
import socket

import Tkinter as tk
from render.render import TexPack
from network.netqueue import NetQueue


class FrameConnect(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent=parent
        self.parent.title("OctoTactics: Connect to a server")
        self.pack(fill=tk.BOTH, expand=1)
    
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
    
    def clear(self):
        self.destroy()
    
    def connect(self):
        """Attempt to connect to the server entered by the user."""
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
                    self.showplayers([tuple(s.split("|")) for s in msg.split(";players:")[1].strip("\n").split(",")])
            except ValueError:
                self.setstatus("Invalid server address")
                raise
                return
            except socket.error:
                self.setstatus("Internal socket error")
                return
    
    def showplayers(self, players):
        self.plist.delete(0, tk.END)
        self.plist.insert(0, ["%s: %s" % p for p in players])
            
    
    def getAddr(self):
        a=self.boxServerAddr.get()
        if a.count(":")>1: raise ValueError
        try:
            h, p=a.split(":")
            return h, int(p) if p!="" else 56239
        except ValueError:
            if a.count(":"): raise
            return (a, 56239)
    
    def setstatus(self, status):
        return self.lbStatus.config(text=status)
            

if __name__=="__main__":
    chdir("..")
    root=tk.Tk()
    fr=FrameConnect(root)
    fr.mkWidgets()
    root.mainloop()