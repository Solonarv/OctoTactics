'''
Created on 07.07.2013

@author: Solonarv
'''
from math import sqrt
def dist_vec(c1,c2):
    return (c1.x-c2.x),(c1.y-c2.y)
def dist_sq(c1,c2):
    dx,dy=dist_vec(c1,c2)
    return dx*dx+dy*dy
def dist(c1,c2):
    return sqrt(dist_sq(c1,c2))
def dampen_transfer(amount,distSq):
    return amount/distSq
