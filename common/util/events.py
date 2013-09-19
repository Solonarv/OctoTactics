'''
Simple event bus system 

Created on 19.09.2013

@author: Solonarv
'''

from util.threads import ReturningThread

class EventBus:
    """
    A simple event bus. You can register event listeners
    that'll be called when a matching event is posted.
    Events can also be posted to this event bus, they can be
    of any type.
    """
    def __init__(self):
        self._listeners = []
    
    def register(self, listener, types):
        """
        Registers the given event listener to this event bus.
        It'll be called when an event E is posted such that
        isinstance(E, types) is True.
        """
        self._listeners.append((listener, types))
    
    def post(self, event):
        """
        Posts an event to this event bus, submitting it for handling
        by all matching listeners. This method will return true iff
        all called listeners do.
        """
        return all([listener(event)
                    for listener, types in self._listeners
                    if isinstance(event, types)])

class ForkingEventBus(EventBus):
    """
    A special kind of event bus that'll create a new thread for
    each listener called, executing them concurrently.
    It'll then join the threads and return the conjunction of each listeners's results.
    """
    def post(self, event):
        threads = [ReturningThread(target = listener, args = (event,))
                   for listener, types in self._listeners
                   if isinstance(event, types)]
        [t.start() for t in threads]
        return all([t.join() for t in threads])

class Event: pass