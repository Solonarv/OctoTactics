'''
Created on 25.09.2013

@author: Solonarv
'''
from server.model.events import PostCellTakeOverEvent
from struct import Struct

class BoardChangeRecorder:
    def __init__(self, board):
        self.changelog = []
        board.EVENT_BUS.register(self.onCellTakeover, PostCellTakeOverEvent)
    
    def onCellTakeover(self, event):
        self.changelog.append(CellOwnerChange(event.subject, event.source,
                                              event.prevowner, event.newowner))

class Change:
    meta_info = Struct('>HH')
    def encode(self): pass
    def pack(self):
        data = self.encode()
        return self.meta_info.pack(self.id, len(data)) + data

class CellOwnerChange(Change):
    id = 0x01
    def __init__(self, subject, source, prevowner, newowner):
        self.subject = subject
        self.source = source
        self.prevowner = prevowner
        self.newowner = newowner

class CellTargetChange(Change):
    id = 0x02
    enc = Struct('>Q8Q')
    def __init__(self, subject, newtargets):
        self.subject = subject.uid
        self.newtargets = tuple(c.uid for c in newtargets)
    
    def encode(self):
        return self.enc.pack(self.subject, *self.newtargets)
        