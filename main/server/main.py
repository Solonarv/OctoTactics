'''
Created on 04.03.2014

@author: Solonarv
'''

from argparse import ArgumentParser
from server.server import Server

parser=ArgumentParser(description="OctoTactics server application")
parser.add_argument("--port", "-p", dest="port", default=56239, type=int, help="The TCP port clients will connect to")

args=parser.parse_args()

server=Server(args.port)