'''
Created on 4 nov. 2013

@author: alex
'''

class Cell:
    celltype=""
    rangeSq=0
    def __init__(self, x, y, owner=None):
        self.x=x
        self.y=y
        self.targets=[]
        self.energy=5
        self.owner=owner
        self.shape=None
        self.counter=None
        self.tarlinepool=set()
    
    def generate_energy(self):
        pass
    
    def transfer_energy(self):
        for target in self.targets:
            self.transfer_to(target)
            
    
    def transfer_to(self, target):
        energy_to_transfer=self.transfer_amount(target)
        if self.energy>energy_to_transfer:
            self.energy-=energy_to_transfer
            if self.owner==target.owner:
                target.energy+=energy_to_transfer
            else:
                target.energy-=energy_to_transfer
                if target.energy<0:
                    target.owner=self.owner
                    target.energy=-target.energy
                
    def update(self):
        self.generate_energy()
        self.transfer_energy()
    
    def transfer_amount(self, target):
        pass

class OctogonCell(Cell):
    celltype="octogon"
    rangeSq=2.2
    maxTargets=3
    def generate_energy(self):
        self.energy+=3.75
    def transfer_amount(self, target):
        nconn=len(self.targets)
        if nconn==1:
            if target.celltype=="octogon":
                return self.energy*.216 # 21.6% of en /turn <=> 15% per second
            else:
                return self.energy*.146 # 14.6% of en/turn <=> 10% per second
        elif nconn==2:
            if target.celltype=="octogon":
                return self.energy*.146 # 14.6% of en/turn <=> 10% per second
            else:
                return self.energy*.11 # 11% of en/turn <=> 7.5% per second
        elif nconn==3:
            if target.celltype=="octogon":
                return self.energy*.122 # 12.2% of en/turn <=> 8.33% per second
            else:
                return self.energy*.098 # 9.8% of en/turn <=> 6.67% per second
            
class SquareCell(Cell):
    rangeSq=1.1
    celltype="square"
    maxTargets=1
    def generate_energy(self):
        self.energy+=3
    def transfer_amount(self, target):
        if target.celltype=="octogon":
            return self.energy*.35 # 35% of en/turn <=> 25% per second
        else:
            return self.energy*.284 # 28.4% of en/turn <=> 20% per second
        
class Board: 
    def __init__(self, width, height):
        self.width=width
        self.height=height
        self.cells={(x,y): SquareCell(x,y,0) if (x+y)%2 else OctogonCell(x,y,0)
                    for x in range(0,width)
                    for y in range(0,height)}
        self.focus=None
        self.focusFrame=None
    
    def tick(self):
        for cell in self.cells.values():
            cell.update()
                
                
                
                
                
    
            
            