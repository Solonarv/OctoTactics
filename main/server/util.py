'''
Created on 04.03.2014

@author: Solonarv
'''

class GameSettings(object):
    def __init__(self):
        self.boardw=10
        self.boardh=8
        self.starts=[]
    
    def encode(self):
        return ("%ix%i|%s\n" % (self.boardw, self.boardh, ','.join(["%s:%ix%i" % (pname, x, y) for (pname, x, y) in self.starts])))