'''
Created on 08.07.2013

@author: Solonarv

Simple test framework: ridiculous interpreter wrapper to play around with modules from
the project loaded
'''
from server.model import Board, Cell

print("Globals are: "+str(globals()))
print("Locals are: "+str(locals()))

vals=[]

class PseudoDict(dict):
    def __init__(self,**additional_mappings):
        super().__init__()
        self.extras=additional_mappings
    def __getitem__(self, *args, **kwargs):
        if(args[0] in self.extras):
            return (self.extras[args[0]])()
        else:
            return dict.__getitem__(self,*args, **kwargs)

loc=PseudoDict(_=lambda: vals[-1],
               __=lambda: vals)
loc.update(Board=Board, Cell=Cell)

while True:
    r=None
    i=input(" >>> ")
    try:
        r=eval(i, globals(), loc)
    except Exception as e:
        print(e)
    print("result %i: %s"%(len(vals)-1,r))
    vals+=[r]