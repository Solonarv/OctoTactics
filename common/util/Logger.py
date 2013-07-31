'''
Created on 07.07.2013

@author: Solonarv
'''

from datetime import date
from util import Enum

Level = Enum("INFO", "WARNING", "ERROR", "SEVERE", "CRITICAL", "STDOUT")

# Module-level shortcuts
def info(s):
    """
    Just informing, nothing of great importance
    """
    logger.log(Level.INFO, s)

def warning(s):
    """
    This just might cause a problem
    """
    logger.log(Level.WARNING, s)

def error(s):
    """
    An error (exception) occurred
    """
    logger.log(Level.ERROR, s)

def severe(s):
    """
    A grave problem has been encountered, crash is quite likely
    """
    logger.log(Level.SEVERE, s)

def critical(s):
    """
    A critical error has been encountered, crash is immediate
    """
    logger.log(Level.CRITICAL, s)

class Logger(object):
    def __init__(self, bufsize = 5):
        # Open file in overwrite mode
        self.logfile = open("cellwars-log-" + date.now().isoformat("-") + ".log", 'w')
        self.bufsize = bufsize
        self.buffer = []
    
    def flush(self):
        for entry in self.buffer:
            self.logfile.write("%s [%s]: %s" % entry)
    
    def log(self, level, msg):
        self.buffer.append((date.now(), level, msg))
        print("%s [%s]: %s" % self.buffer[-1])
        if(len(self.buffer) >= self.bufsize):
            self.flush()
    
logger = Logger()