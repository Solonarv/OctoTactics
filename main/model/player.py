'''
Created on 03.02.2014

@author: Solonarv
'''

class Player(object):
    _hashc=0
    def __init__(self, name="", tex="", hsh=None):
        self.name=name
        self.texpackname=tex
        if hsh==None:
            hsh=Player._hashc
            Player._hashc+=1
        self.id=hsh
    
    def changetex(self, tex):
        self.texpackname=tex