'''
Created on 31.07.2013

@author: Solonarv
'''

from abc import ABCMeta, abstractmethod
from util import Enum

class Server(metaclass=ABCMeta):
    '''
    ABC of server
    '''
    
    STATE = Enum("UNLOADED", "STARTING", "WAITING", "RUNNING", "STOPPING", "STOPPED", "ERRORED")
    
    def __init__(self, name):
        self.state = Server.STATE.UNLOADED
        self.name = name
    
    def start_server(self):
        self.state = Server.STATE.STARTING
    
    def run(self):
        pass
    
    def game_loop(self):
        pass
    
    def game_tick(self):
        pass
    
    @abstractmethod
    def sendUpdates(self):
        pass