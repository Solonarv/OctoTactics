'''
Created on 22.09.2013

@author: Solonarv
'''
from util.events import Event

class BoardEvent(Event):
    def __init__(self, board):
        self.board = board

class CellUpdateEvent(BoardEvent): pass

class EnergyTransferEventBase(BoardEvent):
    def __init__(self, board, src, dest, amount):
        super().__init__(board)
        self.src, self.dest, self.amount = src, dest, amount
    def isagression(self):
        return not self.dest.alliedto(self.src)

class PreTransferEvent(EnergyTransferEventBase): pass

class CellTakeDamageEvent(EnergyTransferEventBase): pass

class CellTakeHealEvent(EnergyTransferEventBase): pass

class CellTakeoverEvent(BoardEvent):
    def __init__(self, board, subject, source, prevowner, newowner):
        super().__init__(board)
        self.subject = subject
        self.source = source
        self.prevowner = prevowner
        self.newowner = newowner
    def ishostile(self):
        return self.prevowner is not None and not self.subject.alliedto(self.newowner)