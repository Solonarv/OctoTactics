'''
Created on 07.07.2013

@author: Solonarv
'''

from itertools import product
from server.model import Cell
from util import Logger
from random import Random

class Board(object):
    def __init__(self, w, h):
        self.cells={}
        self.w=w
        self.h=h
        self.rng=Random()
    def initialize(self,map_otn):
        self.populate()
        self.distr_owners(map_otn)
    def populate(self):
        """Fill the board with unowned (neutral) cells."""
        for x,y in product(range(self.w), range(self.h)):
            if (x+y)%2==0: # x,y both even or both odd
                self.cells[x,y]=Cell.OctogonCell(x,y,None)
            else:
                self.cells[x,y]=Cell.SquareCell(x,y,None)
    def distr_owners(self,map_otn):
        """Randomly distribute cells to owners"""
        if(sum(map_otn.items())>self.x*self.y):
            Logger.warning("Board.distr_owners called, \
            but the board is too small to allocate all the cells!")
        cells=set(self.cells)
        otc={}
        for owner in map_otn:
            s=self.rng.sample(cells, map_otn[owner])
            cells.difference_update(s)
            otc[owner]=s
            for c in s: c.owner=owner
    def tick(self):
        for x,y in self.cells:
            self.cells[x,y].update()