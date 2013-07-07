'''
Created on 07.07.2013

@author: Solonarv
'''
class Cell(object):
    """Cell base class. Is refined into SquareCell and OctogonCell."""
    def __init__(self,x,y,owner):
        self.pos=(x,y)
        self.owner=owner
        self.energy=0
        self.targets=[]
        self.upgrades=[]
        self.lastAttacker=None
        self.lastAssist=None
        self.lastTarget=None
        self.lastTargeter=None
    def owner(self):
        return self.owner
    def energy(self):
        return self.energy
    def alliedTo(self,other):
        return self.owner==other.owner
    def onLivingUpdate(self):
        """Called every game tick, on every single cell."""
        self.generateEnergy()
        self.runUpgrades()
        self.transferEnergy()
    def safeTakeEnergy(self,delta):
        """Take energy from storage, will not reduce below or to 0.\nEverything that uses energy should do the following:
        if(self.safeTakeEnergy(amount):
          # Stuff goes here"""
        if(self.energy >= delta):
            self.energy -= delta
            return True
        return False
    def runUpgrades(self):
        return all(u.run() for u in self.upgrades)
    def transferEnergy(self):
        for tar in self.targets:
            attempt=self.energyToTransfer(tar)
            if(self.safeTakeEnergy(attempt)):
                tar.gainEnergy(self,attempt)
                self.lastTarget=tar
    def energyToTransfer(self,tar): return
    def gainEnergy(self,other,delta):
        if(other==None or self.alliedTo(other)):
            self.energy+=delta
            self.lastAssist=self.lastTargeter=other
        else:
            self.energy-=delta
            if(self.energy<0):
                self.owner=self.lastAttacker.owner
                self.lastAssist=self.lastTargeter=other
                self.lastAttacker=None
            else:
                self.lastAttacker=self.lastTargeter=other