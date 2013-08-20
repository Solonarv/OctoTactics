'''
Created on 19.08.2013

@author: Solonarv
'''

from abc import ABCMeta, abstractmethod, abstractclassmethod
from math import ceil, log
from util.lists import nest

# Cached table of the powers of 2
POWERS = {ex: 2**ex for ex in range(0, 264, 8)}

class Tag(object,metaclass=ABCMeta):
    
    class_ids = {}
    
    @abstractmethod
    def encode(self):
        pass
    @abstractclassmethod
    def decode(cls, data):
        pass
    
    def as_bytes(self):
        return bytearray((self.__class__.id)) + self.encode()
    @staticmethod
    def decode_from(data):
        cls = Tag.class_ids[data[0]]
        return cls.decode(data[1:])

class TagMap(Tag):
    id = 0
    def __init__(self):
        self.values = {}
    
    def __getitem__(self, index):
        return self.values[hash(index)]
    def __setitem__(self, index, val):
        self.values[hash(index)] = val
    def __delitem__(self, index):
        del self.values[hash(index)]
    
    def encode(self):
        result = bytearray()
        for k in self.values:
            v = self.values[k]
            result+= TagInt(k).encode() + v.as_bytes()
    @classmethod
    def decode(cls, data):
        pass
        

class TagList(Tag):
    id = 1
    def __init__(self, type_id):
        self.type_id = type_id
        self.values = []
    
    def addvalues(self, *values):
        self.values+=[v for v in values if isinstance(v, Tag) and v.__class__.id==self.type_id]
    
    def encode(self):
        encoded = (b.as_bytes() for b in self.values)
        return bytearray([self.type_id, len(encoded)] + [TagInt(len(e)).encode() for e in encoded] + [c for e in encoded for c in e])
    @classmethod
    def decode(cls, data):
        type_id, ln = data[0], data[1]
        target = Tag.class_ids[type_id]
        data = data[2:]
        lns = [TagInt.decode(d) for d in (bytearray(it) for it in nest(data[4*ln], 4))]; data = data[4*ln:]
        tags=[]
        for l in lns:
            tags+=target.decode(data[:l])
            data = data[l:]
            
        

class TagByte(Tag):
    id = 2
    def __init__(self, tag_value):
        self.value = int(tag_value) % POWERS[8]
    
    def encode(self):
        return bytearray((self.value,))
    @classmethod
    def decode(cls, data):
        return cls(data[0])

class TagShort(Tag):
    id = 3
    def __init__(self, tag_value):
        self.value = int(tag_value) % POWERS[16]
    
    def encode(self):
        return bytearray((self.value // POWERS[8],
                           self.value % POWERS[8]))
    @classmethod
    def decode(cls, data):
        return cls(data[0]* 256 + data[1])

class TagInt(Tag):
    id = 4
    def __init__(self, tag_value):
        self.value = int(tag_value) % POWERS[32]
    
    def encode(self):
        return bytearray((self.value // POWERS[24],
                          (self.value // POWERS[16]) % POWERS[24],
                          (self.value // POWERS[8]) % POWERS[16],
                          self.value % POWERS[8]))
    @classmethod
    def decode(cls, data):
        return cls(((data[0] * 256 + data[1]) * 256 + data[2]) * 256 + data[3])

class TagBigInt(Tag):
    id = 5
    def __init__(self, tag_value):
        self.value = int(tag_value) % POWERS[256]
        # Length of the integer, in bytes
        self.len = ceil(log(self.value, POWERS[8]))
    
    def encode(self):
        result = bytearray(self.len)
        for p in range(0, self.len, 1):
            result[-p-1] = (self.value // POWERS[p*8]) % POWERS[p*8-8]
        return result
    @classmethod
    def decode(cls, data):
        data=data[1:]
        num = 0
        for i in data:
            num = num * 256 + i
        return cls(num)
        
        

class TagBoolean(Tag):
    id = 6
    def __init__(self, tag_value):
        self.value = bool(tag_value)
    
    def encode(self):
        return bytearray((1 if self.value else 0))
    @classmethod
    def decode(cls, data):
        return cls(data[0])

class TagString(Tag):
    id = 7
    def __init__(self, tag_value):
        self.value = str(tag_value)
    
    def encode(self):
        return bytearray((ord(c) for c in self.value))
    @classmethod
    def decode(cls, data):
        return cls(''.join(chr(i) for i in data))

Tag.class_ids = {TagMap.id: TagMap,
                 TagList.id: TagList,
                 TagByte.id: TagByte,
                 TagShort.id: TagShort,
                 TagBigInt.id: TagBigInt,
                 TagBoolean.id: TagBoolean,
                 TagString.id: TagString}