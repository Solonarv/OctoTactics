'''
Created on 07.07.2013

@author: Solonarv
'''
from math import sqrt
def distVec(c1,c2):
    return (c1.x-c2.x),(c1.y-c2.y)
def distSq(c1,c2):
    dx,dy=distVec(c1,c2)
    return dx*dx+dy*dy
def dist(c1,c2):
    return sqrt(distSq/c1,c2)
def dampenTransfer(amount,distSq):
    return amount/distSq
