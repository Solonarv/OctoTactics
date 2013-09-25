'''
Created on 07.07.2013

@author: Solonarv
'''

from server.model.events import PreTransferEvent, CellTakeDamageEvent, CellTakeHealEvent,\
    CellTakeoverEvent

class Cell(object):
    """Cell base class. Is refined into SquareCell and OctogonCell."""
    def __init__(self,x,y,owner):
        self.pos=(x,y) # The cell's position on the board
        self.owner=owner # Who owns the cell
        self.energy=0 # The amount of energy stored within the cell
        self.targets=[] # Which other cells this cell is attacking
        self.upgrades=[] # Which upgrades are attached to this cell, NYI
        self.last_attacker=None # The last cell to attack this one
        self.last_assist=None # The last cell to help this one
        self.last_target=None # The last cell this cell attacked/helped
        self.last_targeter=None # The last cell that transferred energy to this one
        self.transfertimer = 0
    
    def alliedto(self,other):
        return self.owner==other.owner
    
    def update(self, event):
        """Called every game tick, on every single cell."""
        self.generate_energy(event)
        if self.transfertimer >= self.maxtransfertimer:
            self.transfertimer = 0
            self.transfer_energy(event)
        else:
            self.transfertimer += 1
    
    def transfer_energy(self, cellupdate):
        for tar in self.targets:
            self.transfer_to(cellupdate.board, tar, self.energy_to_transfer(tar))
    
    def transfer_to(self, board, tar, amount):
        if self.energy > amount:
            event = PreTransferEvent(self, board, tar, amount)
            if board.EVENT_BUS.post(event):
                self.energy -= amount
                tar.receive(board, self, amount)
    
    def energy_to_transfer(self, tar): return
    
    def receive(self, board, other, delta):
        if(other==None or self.alliedto(other)):
            if board.EVENT_BUS.post(CellTakeHealEvent(board, other, self, delta)):
                self.energy+=delta
                self.last_assist=self.last_targeter=other
        elif board.EVENT_BUS.post(CellTakeDamageEvent(board, other, self, delta)):
            self.energy-=delta
            if(self.energy<0):
                cto_event = CellTakeoverEvent(board, self, other, self.owner, other.owner)
                if board.EVENT_BUS.post(cto_event):
                    self.owner = cto_event.newowner
                    self.last_assist = self.last_targeter = other
                    self.last_attacker = None
            else:
                self.last_attacker=self.last_targeter=other
        
                
class SquareCell(Cell):
    defaultrange=1.5
    maxenergy=80
    maxcontacts=1
    maxtransfertimer = 20
    
    def __init__(self,x,y,owner):
        super().__init__(x,y,owner)
        self.range=SquareCell.default_range
    
    def generate_energy(self):
        if self.energy < self.maxenergy:
            self.energy+=.25 # .25 e/tick = 5 e/sec
    
    # BETA -- currently not enough information to balance
    def energy_to_transfer(self,tar):
        if isinstance(tar, SquareCell):
            return self.energy * .2 # 20 %e/20sec
        elif isinstance(tar, OctogonCell):
            return self.energy * .25 # 25 %e/20sec
        else:
            return 0

class OctogonCell(Cell):
    defaultrange=1.5
    maxenergy=200
    maxcontacts=3
    maxtransfertimer = 20
    
    def __init__(self,x,y,owner):
        super().__init__(x,y,owner)
        self.range=SquareCell.default_range
    
    def generate_energy(self):
        if self.energy < self.maxenergy:
            self.energy+=.1 # .1e/tick = 2 e/sec
    
    # BETA -- currently not enough information to balance
    def energy_to_transfer(self,tar):
        nTars=len(self.targets)
        if isinstance(tar, SquareCell):
            return (self.energy * .1 if nTars==1 else # 10 %e/20sec
                self.energy * .075 if nTars==2 else # 7.5 %e/20sec
                self.energy * .0666 if nTars==3 else # 6.66 %e/20sec
                0)
        elif isinstance(tar, OctogonCell):
            return (self.energy * .15 if nTars==1 else # 15 %e/20sec
                self.energy * .1 if nTars==2 else # 10 %e/20sec
                self.energy * .0833 if nTars==3 else # 8.33 %e/20sec
                0)
        else:
            return 0