'''
Created on 4 nov. 2013

@author: alex
'''

class Cell:
    def __init__(self, x, y, owner):
        self.x=x
        self.y=y
        self.targets=[]
        self.energy=5
        self.owner=owner
    
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
                
    def transfer_amount(self, target):
        pass
    
    
            
            