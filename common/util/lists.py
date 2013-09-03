'''
Created on 20.08.2013

@author: Solonarv
'''

def cluster(lst, size):
    """
    Clusters an iterable into a tuple of nested tuples of length size, i.e.
    lists.cluster( (a, b, c, d, e, f, g, h, i), 3) =>
      ((a, b, c), (d, e, f), (g, h, i))
    """
    return zip(*[iter(lst)]*size)
        