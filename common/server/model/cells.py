'''
Created on 07.07.2013

@author: Solonarv
'''

from util import geometry

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
    def allied_to(self,other):
        return self.owner==other.owner
    def update(self):
        """Called every game tick, on every single cell."""
        self.generate_energy()
        self.run_upgrades()
        self.transfer_energy()
    def safe_take_energy(self,delta):
        """Take energy from storage, will not reduce below or to 0.\nEverything that uses energy should do the following:
        if(self.safe_take_energy(amount):
          # Stuff goes here"""
        if(self.energy >= delta):
            self.energy -= delta
            return True
        return False
    def run_upgrades(self):
        return all(u.run() for u in self.upgrades)
    def transfer_energy(self):
        for tar in self.targets:
            attempt=self.energy_to_transfer(tar)
            if(self.safe_take_energy(attempt)):
                tar.gain_energy(self,attempt)
                self.last_target=tar
    def energy_to_transfer(self,tar): return
    def gain_energy(self,other,delta):
        if(other==None or self.allied_to(other)):
            self.energy+=delta
            self.last_assist=self.last_targeter=other
        else:
            self.energy-=delta
            if(self.energy<0):
                self.owner=self.last_attacker.owner
                self.last_assist=self.last_targeter=other
                self.last_attacker=None
            else:
                self.last_attacker=self.last_targeter=other
    def toBinary(self) -> bytearray:
        b = bytearray()
        
        return b
                
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
        if(tar is SquareCell):
            raw=self.energy * .011 # 1.1 %e/tick = 20 %e/sec
        elif(tar is OctogonCell):
            raw=self.energy * .014 # 1.4 %e/tick = 25 %e/sec
        else:
            return 0
        return geometry.dampen_transfer(raw,self.distSq(tar))

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
        if(tar is SquareCell):
            raw=(self.energy * .0053 if nTars==1 else # .53 %e/tick = 10 %e/sec
                self.energy * .0039 if nTars==2 else # .39 %e/tick = 7.5 %e/sec
                self.energy * .0034 if nTars==3 else # .34 %e/tick = 6.66 %e/sec
                0)
        elif(tar is OctogonCell):
            raw=(self.energy * .0081 if nTars==1 else # .81 &e/tick = 15 %e/sec
                self.energy * .0053 if nTars==2 else # .53 %e/tick = 10 %e/sec
                self.energy * .0043 if nTars==3 else # .43 %e/tick = 8.33 %e/sec
                0)
        else:
            return 0
        return geometry.dampen_transfer(raw,self.distSq(tar))