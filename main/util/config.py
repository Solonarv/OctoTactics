'''
Created on 29.10.2013

@author: Solonarv
'''

from string import punctuation

class Settings:
    """
    A class to store settings. Can be modified,
    uses a 2-level hierarchical structure.
    """
    def __init__(self):
        self.data = {}
    
    # Emulate sequence by wrapping self.data
    def __len__(self, *args, **kwargs): return self.data.__len__(*args, **kwargs)
    def __getitem__(self, *args, **kwargs): return self.data.__getitem__(*args, **kwargs)
    def __setitem__(self, *args, **kwargs): return self.data.__setitem__(*args, **kwargs)
    def __iter__(self, *args, **kwargs): return self.data.__iter__(*args, **kwargs)
    def __reversed__(self, *args, **kwargs): return self.data.__reversed__(*args, **kwargs)
    def __contains__(self, *args, **kwargs): return self.data.__contains__(*args, **kwargs)
    
    def mergefrom(self, src):
        for key in src:
            if key not in self:
                self[key] = SettingsCategory(key)
            self[key].mergefrom(src[key])
    
    def fromfile(self, filename):
        with open(filename, "r") as file:
            self._fromfile(file)
    
    def _fromfile(self, fileobj):
        subcat = ""
        for line in fileobj:
            
            line = line.partition('#')[0].strip() # Ignore everything after a '#'
            if line == "": continue
            if line[:-1]==":":
                subcat = line[:-1].strip()
                if subcat not in self:
                    self[subcat] = SettingsCategory(subcat)
            elif subcat!="" and "=" in line:
                key, _, rval = line.partition("=")
                # Value type is explicit
                if rval[1]=="%":
                    t = rval[0].lower()
                    if t=="i": val = int(rval[2:])
                    elif t=="f": val = float(rval[2:])
                    elif t=="b": val = bool(rval[2:])
                    else: val = rval[2:]
                # Automatically determine value type
                else:
                    val=parsestr(rval)
                self[subcat][key]=val
                


class SettingsCategory:
    """
    Stores the settings in a category, and its name.
    """
    def __init__(self, name):
        self.name = name
        self.data = {}
    
    # Emulate dictionary by wrapping self.data
    def __len__(self, *args, **kwargs): return self.data.__len__(*args, **kwargs)
    def __getitem__(self, *args, **kwargs): return self.data.__getitem__(*args, **kwargs)
    def __setitem__(self, *args, **kwargs): return self.data.__setitem__(*args, **kwargs)
    def __iter__(self, *args, **kwargs): return self.data.__iter__(*args, **kwargs)
    def __contains__(self, *args, **kwargs): return self.data.__contains__(*args, **kwargs)
    
    def mergefrom(self, src):
        for key in src:
            self.data[key]=src[key]
    

parsestr = lambda s: s.lower()=="true" or (False if s.lower()=="false" else
                                           int(s) if s.isdigit() else
                                           float(s) if len(set(punctuation).intersection(s)) == 1 and
                                                    s.count('.')==1
                                           else s)