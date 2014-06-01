'''
Created on 22.08.2013

@author: Solonarv
'''
from twisted.protocols import basic

class DelegatingChannelProtocol(basic.LineReceiver):
    """
    A Twisted protocol that delegates message handling to another object, passing channel hierarchy
    and message separately. By default, expects messages of the form:
    
    channel/subchannel/subsubchannel:message of whatever
    
    This'll call:
    
    self.msghandler.handler(self, ['channel','subchannel','subsubchannel'], 'message of whatever')
    
    msghandler is passed in at protocol instantiation. 
    
    """
    def __init__(self, factory, msghandler, msgstart=":", chandelim="/"):
        self.factory=factory
        self.msghandler=msghandler
        self.msgstart=msgstart
        self.chandelim=chandelim
    
    def lineReceived(self, line):
        chan, msg = None,None
        try:
            chan, msg = line.split(self.msgstart)
            chan = chan.split(self.chandelim)
        except ValueError: # split() failed => invalid message; print and ignore
            print "Received invalid line from: %s" % (line)
            return
        self.msghandler.handle(self, chan, msg)

class DCMessageHandlerBase(object):
    
    def handle(self, protocol, chan, msg):
        pass