'''
Created on 19.09.2013

@author: Solonarv
'''

from itertools import product
from random import Random
from server.model import cells
from server.model.events import CellUpdateEvent
from util import logger
from util.events import EventBus

class Board(object):
    def __init__(self, w, h):
        self.cells={}
        self.w=w
        self.h=h
        self.rng=Random()
        self.EVENT_BUS = EventBus()
    
    def register_handlers(self, server):
        server.EVENT_BUS.register(self.onTick)
    
    def onTick(self, event):
        for c in product(range(0, self.w), range(0, self.h)):
            self.cells[c].update(CellUpdateEvent(self))
        return True
    
    def fill(self):
        for x,y in product(range(0, self.w), range(0, self.h)):
            self.cells[x,y] = (cells.SquareCell(x, y, None) if (x+y) % 2
                               else cells.OctogonCell(x, y, None))