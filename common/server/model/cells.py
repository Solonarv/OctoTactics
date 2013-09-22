'''
Created on 07.07.2013

@author: Solonarv
'''

from server.model.events import PreTransferEvent, CellTakeDamageEvent, CellTakeHealEvent

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
    
    def alliedto(self,other):
        return self.owner==other.owner
    
    def update(self, event):
        """Called every game tick, on every single cell."""
        self.generate_energy(event)
        self.transfer_energy(event)
    
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
                self.owner=self.last_attacker.owner
                self.last_assist=self.last_targeter=other
                self.last_attacker=None
            else:
                self.last_attacker=self.last_targeter=other
                
class SquareCell(Cell):
    default_range=1.5
    max_energy=80
    max_contacts=1
    
    def __init__(self,x,y,owner):
        super().__init__(x,y,owner)
        self.range=SquareCell.default_range
    
    def generate_energy(self):
        self.energy+=.25 # .25 e/tick = 5 e/sec
    
    # BETA -- currently not enough information to balance
    def energy_to_transfer(self,tar):
        if isinstance(tar, SquareCell):
            return self.energy * .011 # 1.1 %e/tick = 20 %e/sec
        elif isinstance(tar, OctogonCell):
            return self.energy * .014 # 1.4 %e/tick = 25 %e/sec
        else:
            return 0

class OctogonCell(Cell):
    default_range=1.5
    max_energy=200
    max_contacts=3
    
    def __init__(self,x,y,owner):
        super().__init__(x,y,owner)
        self.range=SquareCell.default_range
    
    def generate_energy(self):
        self.energy+=.1 # .1e/tick = 2 e/sec
    
    def energy_to_transfer(self,tar):
        nTars=len(self.targets)
        if isinstance(tar, SquareCell):
            return (self.energy * .0053 if nTars==1 else # .53 %e/tick = 10 %e/sec
                self.energy * .0039 if nTars==2 else # .39 %e/tick = 7.5 %e/sec
                self.energy * .0034 if nTars==3 else # .34 %e/tick = 6.66 %e/sec
                0)
        elif isinstance(tar, OctogonCell):
            return (self.energy * .0081 if nTars==1 else # .81 &e/tick = 15 %e/sec
                self.energy * .0053 if nTars==2 else # .53 %e/tick = 10 %e/sec
                self.energy * .0043 if nTars==3 else # .43 %e/tick = 8.33 %e/sec
                0)
        else:
            return 0