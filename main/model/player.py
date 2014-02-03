'''
Created on 03.02.2014

@author: Solonarv
'''

class Player:
    def __init__(self, name, tex):
        self.name=name
        self.texpack=tex
    
    def changetex(self, tex):
        self.texpack=tex

class PlayerClient(Player): pass