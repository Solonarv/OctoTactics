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
    
    def draw(self,can):
        if self.shape is None:
            if self.celltype=="octogon":
                self.shape=can.create_oval(self.x*30,self.y*30,self.x*30+30,self.y*30+30)
            else:
                self.shape=can.create_rectangle(self.x*30,self.y*30,self.x*30+30,self.y*30+30)
        if self.counter is None:
            self.counter=can.create_text(self.x*30+15,self.y*30+15, text=int(self.energy), anchor="center")
        else:
            can.itemconfig(self.counter,text=int(self.energy))

        for tar,lines in self.targets:
            if lines is not None:
                for i,l in enumerate(lines):
                    rx=0 if i==0 else 20 if i==1 else 10
                    ry=20 if i==0 else 10
                    if l is None:
                        l=can.create_line(self.x*30+rx,self.y+ry,tar.x,tar.y)
                    else:
                        can.coords(l,self.x*30+rx,self.y+ry,tar.x,tar.y)
            

class OctogonCell(Cell):
    celltype="octogon"
    rangeSq=2
    maxTargets=3
    def generate_energy(self):
        self.energy+=0.025
    def transfer_amount(self, target):
        nconn=len(self.targets)
        if nconn==1:
            if target.celltype=="octogon":
                return self.energy*.0081 # .81% of en /tick <=> 15% per second
            else:
                return self.energy*.0053 # .53% of en/tick <=> 10% per second
        elif nconn==2:
            if target.celltype=="octogon":
                return self.energy*.0053 # .53% of en/tick <=> 10% per second
            else:
                return self.energy*.0039 # .39% of en/tick <=> 7.5% per second
        elif nconn==3:
            if target.celltype=="octogon":
                return self.energy*.0043 # .43% of en/tick <=> 8.33% per second
            else:
                return self.energy*.0034 # .34% of en/tick <=> 6.67% per second
            
class SquareCell(Cell):
    rangeSq=1.1
    celltype="square"
    maxTargets=1
    def generate_energy(self):
        self.energy+=0.1
    def transfer_amount(self, target):
        if target.celltype=="octogon":
            return self.energy*.014 # 1.4% of en/tick <=> 25% per second
        else:
            return self.energy*.011 # 1.1% of en/tick <=> 20% per second
        
class Board:
    def __init__(self, width, height):
        self.width=width
        self.height=height
        self.cells={(x,y): SquareCell(x,y) if (x+y)%2 else OctogonCell(x,y)
                    for x in range(0,width)
                    for y in range(0,height)}
    
    def tick(self):
        for cell in self.cells.values():
            cell.update()
        
    def draw(self,can):
        for cell in self.cells.values():
            cell.draw(can)
                
                
                
                
                
    
            
            