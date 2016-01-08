'''
Created on 04.03.2014

@author: Solonarv
'''

from argparse import ArgumentParser
from server import Server
from twisted.internet import reactor

parser=ArgumentParser(description="OctoTactics server application")
parser.add_argument("--port", "-p", dest="port", default=56239, type=int, help="The TCP port clients will connect to")
parser.add_argument("--maxplayers", "-mp", dest="maxplayers", default=2, type=int, help="The maximum number of players")

args=parser.parse_args()


print "Server started on port %i with %i max. players" % (args.port, args.maxplayers)
server=Server(args.maxplayers)


# Eclipse is a derp, these lines work fine
reactor.listenTCP(args.port, server)
reactor.run()