'''
Created on 19.09.2013

@author: Solonarv
'''
from threading import Thread

class ReturningThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super().__init__(group, target, name, args, kwargs, verbose)
        self._result = object()
        self._result.isset = False
    
    def run(self):
        try:
            if self._target:
                self._result.val = self._target(*self._args, **self._kwargs)
                self._result.isset = True
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs
    
    def join(self, timeout = None):
        super().join(timeout)
        return self._result.val if self._result.isset else None