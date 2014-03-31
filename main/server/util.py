'''
Created on 04.03.2014

@author: Solonarv
'''

class GameSettings(object):
    def __init__(self):
        self.boardw=10
        self.boardh=8
        self.starts=[]
        self.ops=[]
    
    def encode(self):
        return "%ix%i|%s|%s" % (self.boardw,
                               self.boardh,
                               ','.join([("%s:%ix%i" % (pname, x, y)) for (pname, x, y) in self.starts]),
                               ','.join([p.name for p in self.ops]))
    
    def setoption(self, opt, args):
        if   opt=="boardw":
            try: self.boardw=int(args)
            except ValueError: pass
        elif opt=="boardh":
            try: self.boardh=int(args)
            except ValueError: pass
        elif opt=="addstart":
            try:
                player, x, y=args.split(",")
                self.starts.append((player, int(x), int(y)))
            except ValueError: pass
        elif opt=="removestart":
            try:
                player, x, y=args.split(",")
                self.starts.remove((player, int(x), int(y)))
            except ValueError: pass
        elif opt=="removestarts":
            for (pname, x, y) in self.starts:
                if pname==args: self.starts.remove((pname, x, y))