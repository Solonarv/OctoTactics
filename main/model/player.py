'''
Created on 03.02.2014

@author: Solonarv
'''

class Player(object):
    def __init__(self, name, tex):
        self.name=name
        self.texpackname=tex
    
    def changetex(self, tex):
        self.texpackname=tex