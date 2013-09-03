'''
Created on 22.08.2013

@author: Solonarv
'''
from server.model.cells import Cell
from abc import ABCMeta, abstractmethod, abstractclassmethod

class Packet(object, metaclass=ABCMeta):
    def __init__(self, tp): self.tp = tp
    @abstractmethod
    def toBinary(self) -> bytearray:
        return bytearray((self.tp,))
        

class Packet001Cell(Packet):
    def __init__(self, cell : Cell):
        self.cell = cell
    @abstractmethod
    def toBinary(self) -> bytearray:
        b = Packet.toBinary(self)
        b.extend((self.data.pos[0], self.data.pos[1]))