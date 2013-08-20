'''
Created on 20.08.2013

@author: Solonarv
'''

def nest(lst, length):
    i = 0
    while True:
        r=zip(lst[i:], range(length))
        i+=len(r)
        if r:
            yield (e for e,_ in r)
        else:
            break