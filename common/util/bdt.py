'''
Created on 02.09.2013

@author: Solonarv

Classes to represent data in a binary format.
Name is BDT = Binary Data Tags
'''

import gzip
from util import Enum
json = None

data_types = Enum(("END", "BYTE", "SHORT", "INT", "LONG", "STRING", "LIST", "COMPOUND",))

class BDTBase:
    """
    ABC of all types of binary data tag
    """
    enc_len = 0
    def __init__(self, tp):
        """
        The super constructor only stores the tag's type
        """
        self.tp = tp
    def encode(self, compress=0):
        """
        Encode a tag to binary representation.
        Optional compress argument indicates gzip compress level (1-9).
        Default value is0, means don't compress.
        """
        raw = bytes(self._encode())
        return gzip.compress(raw, compress) if compress else raw
    def _encode(self) -> bytearray:
        """
        Abstract method to do the actual encoding
        """
        return bytearray((self.tp,))
    @classmethod
    def decode(cls, data):
        tp = data[0]
        if tp == data_types.END:
            return BDTEnd()
        elif tp == data_types.BYTE:
            return BDTByte(data[1])
        elif tp == data_types.SHORT:
            return BDTShort.decode(data[1:])
        elif tp == data_types.INT:
            return BDTInt.decode(data[1:])
        elif tp == data_types.LONG:
            return BDTLong.decode(data[1:])
        elif tp == data_types.STRING:
            return BDTString.decode(data[1:])
        elif tp == data_types.LIST:
            return BDTList.decode(data[1:])
        elif tp == data_types.COMPOUND:
            return BDTCompound.decode(data[1:])
        

class BDTCompound(BDTBase):
    """
    Tag that stores a String -> Tag mapping
    It's encoded as an association list in binary form
    """
    def __init__(self):
        super().__init__(data_types.COMPOUND)
        self._entries = {}
    
    def put_tag(self, key, tag):
        """
        Store a tag inside this compound tag
        """
        self._entries[key] = tag
    def put_byte(self, key, val):
        self.put_tag(key, BDTByte(val))
    def put_short(self, key, val):
        self.put_tag(key, BDTShort(val))
    def put_int(self, key, val):
        self.put_tag(key, BDTInt(val))
    def put_long(self, key, val):
        self.put_tag(key, BDTLong(val))
    def put_string(self, key, val):
        self.put_tag(key, BDTString(val))
    
    def get_tag(self, key):
        """
        Retrieves a tag from this compound tag
        """
        return self._entries[key]
    def get_integral(self, key):
        """
        Retrieves a byte, short, int or long from this compound tag
        (depending on what's stored)
        """
        tag = self.get_tag(key)
        if isinstance(tag, (BDTByte, BDTShort, BDTInt, BDTLong)):
            return tag.val
        else:
            raise KeyError("No integral value for key %s found in BDTCompound @%#x" % (key, id(self)))
    
    def get_string(self, key):
        """
        Retrieves a string from this ompound tag
        """
        tag = self.get_tag(key)
        if isinstance(tag, BDTString):
            return tag.val
        else:
            raise KeyError("No string value for key %s found in BDTCompound @%#x" % (key, id(self)))
    
    def _encode(self)->bytearray:
        b = BDTBase._encode(self)
        b += bytearray(len(self._entries).to_bytes(4, 'big'))
        for k in self._entries:
            enc = self._entries[k]._encode()
            b += BDTString(k)._encode()[1:] + bytearray(len(enc).to_bytes(4, 'big')) + enc
        return b
    @classmethod
    def decode(cls, data) -> BDTBase:
        target = cls()
        ln = int.from_bytes(bytes(data[:4]), 'big')
        data = data[4:]
        for _ in range(ln):
            sl = int.from_bytes(data[:2], 'big')
            k = BDTString.decode(data[:sl+2]).val
            data = data[sl+2:]
            el = int.from_bytes(data[:4], 'big')
            v = BDTBase.decode(data[:el+4])
            data = data[el+4:]
            target.put_tag(k, v)

class BDTList(BDTBase):
    """
    Tag that stores a list of other tags of same type
    """
    def __init__(self, tp_id):
        super().__init__(data_types.LIST)
        self._entries = []
        self.target_tp = tp_id
    def add_tag(self, tag):
        if tag.tp == self.target_tp: self._entries.append(tag)
    def __getitem__(self, *args, **kwargs): return self._entries.__getitem__(*args, **kwargs)
    def __delitem__(self, *args, **kwargs): return self._entries.__delitem__(*args, **kwargs)
    def __iter__(self, *args, **kwargs): return self._entries.__iter__(*args, **kwargs)
    
    def _encode(self)->bytearray:
        b = BDTBase._encode(self)
        b += bytearray((self.target_tp,))
        save_lengths = (tpid_to_class[self.target_tp].enc_len > 0)
        for e in self._entries:
            enc = e._encode()[1:] # Strip type indicator from encoded entry
            if save_lengths: b += bytearray(len(enc).to_bytes(4, 'big'))
            b += enc
        return b
    @classmethod
    def decode(cls, data):
        ls = cls(data[0]); data = data[1:]
        tar_class = tpid_to_class[ls.target_tp]
        enc_len = tar_class.enc_len
        while data:
            dat = bytearray()
            if enc_len > 0:
                dat = data[:enc_len]
                data = data[enc_len:]
            else:
                l = int.from_bytes(data[:4], 'big')
                dat = data[4:l+4]
                data = data[l+4:]
            ls.add_tag(tar_class.decode(dat))

class BDTEnd(BDTBase):
    """
    Tag used to signify the end of a tag compound or a list
    """
    def __init__(self): super().__init__(data_types.END)
    
    def _encode(self)->bytearray:
        return BDTBase._encode(self)

class BDTIntegral(BDTBase):
    """
    Base class of classes returned by BDTIntegral_ClassFactory.
    Tag that stores an integer value of some length
    """

def BDTIntegral_ClassFactory(int_len, tp_id, name = None):
    """
    Subclass BDTIntegral to create a tag holding an integer value
    of some length. Metaprogramming FTW!
    """
    if name is None:
        name = "BDTIntegral_len%i" % int_len
    doc = "\nTag that stores a %i-byte (%i bit) integer value.\n" % (int_len, int_len * 8)
    class result(BDTIntegral):
        __doc__ = doc
        def __init__(self, val):
            super().__init__(self.tp_id)
            self.val = val % 256**self.int_len
        
        def _encode(self)->bytearray:
            return BDTBase._encode(self) + self.val.to_bytes(self.int_len)
        @classmethod
        def decode(cls, data) -> BDTBase:
            return cls(int.from_bytes(data, 'big'))
    result.__name__ = name
    result.int_len = int_len
    result.tp_id = tp_id
    result.enc_len = int_len
    return result

BDTByte = BDTIntegral_ClassFactory(1, data_types.BYTE, "BDTByte")
BDTShort = BDTIntegral_ClassFactory(2, data_types.SHORT, "BDTShort")
BDTInt = BDTIntegral_ClassFactory(4, data_types.INT, "BDTInt")
BDTLong = BDTIntegral_ClassFactory(8, data_types.LONG, "BDTLong")

class BDTString(BDTBase):
    """
    Tag that stores a string up to 65535 chars long
    """
    def __init__(self, val):
        super().__init__(data_types.STRING)
        self.val = str(val)[:0x10000]
    
    def _encode(self)->bytearray:
        return BDTBase._encode(self) \
            + bytearray(len(self.val).to_bytes(2, 'big')) \
            + bytearray(self.val, 'utf8')
    @classmethod
    def decode(cls, data):
        ln = int.from_bytes(data[:2], 'big')
        return BDTString(data[2:2+ln].decode("utf8"))

tpid_to_class = [BDTEnd, BDTByte, BDTShort, BDTInt, BDTLong, BDTString, BDTList, BDTCompound]