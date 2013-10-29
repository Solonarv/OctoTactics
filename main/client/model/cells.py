'''
Created on 12.07.2013

@author: Solonarv
'''
from util import Enum
from itertools import product

class CellData:
    TYPE = Enum(("OCTOGON", "SQUARE"))
    
    def __init__(self,x,y,owner,tp,uid):
        self.pos = (x,y)
        self.owner = owner
        self.energy = 0
        self.targets = []
        self.upgrades = []
        self.last_attacker = None
        self.last_assist = None
        self.last_target = None
        self.last_targeter = None
        self.tp = tp
        self.uid = uid

class BoardData:
    def __init__(self, w, h):
        self.cells = {(x,y): None for x,y in product(range(x), range(y))}
        