'''
Created on 16.10.2013

@author: Solonarv
'''
import abc

def find_main_superclass(cls):
    for clazz in cls.__bases__:
        if isinstance(clazz, SubtypedMeta):
            return find_main_superclass(clazz)
    return None
    

class SubtypedMeta(type):
    
    def __new__(meta, name, bases, namespace, **kwargs):
        cls = super().__new__(meta, name, bases, namespace)
        
        main_superclass = find_main_superclass(cls)
        if main_superclass is None:
            cls._named_subtypes = {}
        elif "id" in kwargs:
            tpid = kwargs["id"]
            if tpid not in main_superclass._named_subtypes:
                main_superclass._named_subtypes[tpid] = cls
        
        return cls
    
    def getsubclass(self, tpid):
        return self._named_subtypes.get(tpid, None)