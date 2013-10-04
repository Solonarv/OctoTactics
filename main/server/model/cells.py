'''
Created on 07.07.2013

@author: Solonarv
'''

from server.model.events import PreTransferEvent, CellTakeDamageEvent, CellTakeHealEvent,\
    PreCellTakeOverEvent, PostCellTakeOverEvent, PreCellRetargetEvent,\
    PostCellRetargetEvent

class Cell(object):
    """Cell base class. Is refined into SquareCell and OctogonCell."""
    nextUID = 0
    tpid = 0
    def __init__(self, x, y, owner, board):
        self.pos = (x,y) # The cell's position on the board
        self.owner = owner # Who owns the cell
        self.energy = 0 # The amount of energy stored within the cell
        self.targets = [] # Which other cells this cell is attacking
        self.upgrades = [] # Which upgrades are attached to this cell, NYI
        self.last_attacker = None # The last cell to attack this one
        self.last_assist = None # The last cell to help this one
        self.last_target = None # The last cell this cell attacked/helped
        self.last_targeter = None # The last cell that transferred energy to this one
        self.transfertimer  =  0
        self.uid  =  self.nextUID
        self.nextUID += 1
        self.board = board
    
    def alliedto(self, other):
        """
        Indicates whether or not this cell is allied to another.
        Ideally, this method should be reflective, i.e. x.alliedto(y) == y.alliedto(x)
        in all cases.
        """
        return self.owner == other.owner
    
    def update(self, event):
        """
        Called every game tick, on every single cell.
        Causes the cell to update itself, performing a step
        of the simulation.
        
        Fires:
         - self.transfer_energy's events, indirectly.
        """
        self.generate_energy(event)
        if self.transfertimer >= self.maxtransfertimer:
            self.transfertimer = 0
            self.transfer_energy(event)
        else:
            self.transfertimer += 1
    
    def transfer_energy(self, cellupdate):
        """
        Perform all energy transfers that should occur in a given tick.
        
        Fires:
         - self.transfer_to's events, indirectly.
        """
        for tar in self.targets:
            self.transfer_to(tar, self.energy_to_transfer(tar))
    
    def transfer_to(self, tar, amount):
        """
        Transfers a given amount of energy to a given target cell.
        The target cell is left to handle that energy influx.
        
        Fires:
         - PreTransferEvent, before the transfer occurs
         - PostTransferEvent, after the transfer occurs.
         - Whatever tar.receive_energy fires
        """
        if self.energy > amount:
            event = PreTransferEvent(self, self.board, tar, amount)
            if self.board.EVENT_BUS.post(event):
                self.energy -= amount
                tar.receive_energy(self.board, self, amount)
    
    def energy_to_transfer(self, tar): return
    
    def receive_energy(self, other, delta):
        """
        Receives a given amount of energy from another cell.
        Self will lose energy from an enemy transfer and gain energy
        from an allied transfer, and fire appropriate events.
        
        Fires:
         - CellTakeHealEvent, before applying an energy gain.
         - CellTakeDamageEvent, before applying an energy loss
         - PreCellTakeOverEvent, before transferring ownership to a conqueror
         - PostCellTakeOverEvent, after transferring ownership
        
        TODO: Transform CellTakeDamage/HealEvent to Base/Pre/Post form
        """
        if(other==None or self.alliedto(other)):
            if self.board.EVENT_BUS.post(CellTakeHealEvent(self.board, other, self, delta)):
                self.energy+=delta
                self.last_assist=self.last_targeter=other
        elif self.board.EVENT_BUS.post(CellTakeDamageEvent(self.board, other, self, delta)):
            self.energy-=delta
            if(self.energy<0):
                cto_event = PreCellTakeOverEvent(self.board, self, other, self.owner, other.owner)
                if self.board.EVENT_BUS.post(cto_event):
                    self.owner = cto_event.newowner
                    self.last_assist = self.last_targeter = other
                    self.last_attacker = None
                self.board.EVENT_BUS.post(PostCellTakeOverEvent.frompre(cto_event))
            else:
                self.last_attacker=self.last_targeter=other
    
    def retarget(self, newtargets):
        """
        Changes self's targets (cells energy is being transferred to) to those
        given in newtargets. Range and max connections checks are made here.
        
        Fires:
         - PreCellRetargetEvent, before changing targets
         - PostCellRetargetEvent, after changing targets
        """
        targets = [tar for tar in newtargets
                        if (self.defaultrange*self.defaultrange)
                        >= (self.pos[0] - tar.pos[0]) * (self.pos[0] - tar.pos[0]) +
                        (self.pos[1] - tar.pos[1]) * (self.pos[1] - tar.pos[1])][:self.maxcontacts]
        cr_event = PreCellRetargetEvent(self.board, self, self.targets, targets)
        if self.board.EVENT_BUS.post(cr_event):
            self.targets = targets
            self.board.EVENT_BUS.post(PostCellRetargetEvent.frompre(cr_event))
            
                
class SquareCell(Cell):
    defaultrange=1.3 # Enough to reach cells at Chebyshev distance of 1 and no others.
    maxenergy=80
    maxcontacts=1
    maxtransfertimer = 20
    tpid = 1
    
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
    defaultrange=1.5 # Enough to reach cells at Manhattan distance of 1, and no others.
    maxenergy=200
    maxcontacts=3
    maxtransfertimer = 20
    tpid = 2
    
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