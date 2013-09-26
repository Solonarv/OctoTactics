'''
Created on 25.09.2013

@author: Solonarv
'''
from server.model.events import PostCellTakeOverEvent

class BoardChangeRecorder:
    def __init__(self, board):
        self.changelog = []
        board.EVENT_BUS.register(self.onCellTakeover, PostCellTakeOverEvent)
    
    def onCellTakeover(self, event):
        self.changelog.append(CellOwnerChange(event.subject, event.source,
                                              event.prevowner, event.newowner))

class Change: pass

class CellOwnerChange(Change):
    def __init__(self, subject, source, prevowner, newowner):
        self.subject = subject
        self.source = source
        self.prevowner = prevowner
        self.newowner = newowner