'''
Created on 07.07.2013

@author: Solonarv
'''
from lib.cell.CellBase import Cell
from lib.util import AbstractGeometry 

class SquareCell(Cell):
    defaultRange=1.5
    maxEnergy=80
    maxContacts=1
    def __init__(self,x,y,owner):
        super().__init__(x,y,owner)
        self.range=SquareCell.defaultRange
    def generateEnergy(self):
        self.energy+=.25 # .25 e/tick = 5 e/sec
    # BETA -- currently not enough information to balance
    def energyToTransfer(self,tar):
        if(tar is SquareCell):
            raw=self.energy * .011 # 1.1 %e/tick = 20 %e/sec
        elif(tar is OctogonCell):
            raw=self.energy * .014 # 1.4 &e/tick = 25 %e/sec
        else:
            return 0
        return AbstractGeometry.dampenTransfer(raw,self.distSq(tar))

class OctogonCell(Cell):
    defaultRange=1.5
    maxEnergy=200
    maxContacts=3
    def __init__(self,x,y,owner):
        super().__init__(x,y,owner)
        self.range=SquareCell.defaultRange
    def generateEnergy(self):
        self.energy+=.1 # .1e/tick = 2 e/sec
    def energyToTransfer(self,tar):
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
        return AbstractGeometry.dampenTransfer(raw,self.distSq(tar))