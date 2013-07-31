'''
Created on 12.07.2013

@author: Solonarv
'''

class CellData:
    def __init__(self,x,y,owner):
        self.pos=(x,y)
        self.owner=owner
        self.energy=0
        self.targets=[]
        self.upgrades=[]
        self.last_attacker=None
        self.last_assist=None
        self.last_target=None
        self.last_targeter=None
        