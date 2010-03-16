# -*- coding: utf-8 -*-
"""
A reusable synchronization decorator implementation. It is using reentrant locks to synchronize
subsequent calls of the specified functions.
"""
from __future__ import with_statement

import sys
from threading import RLock
from functools import wraps
 

def synchronized(func=None, lock=None):
    """ synchronization decorator. 
    
        lock - the user can specify a concrete lock object to be used 
               with this specific synchronization decorator. This is 
               useful when a group of functions should be synchronized
               together.
    """

    # the decarator can be used with an argument as well as without any 
    if func is None:
        def wrapper(f):
            return synchronized(f, lock=lock)
        return wrapper
 
    _lock = lock if lock else RLock()

    @wraps(func)
    def wrapper(*args, **kwargs):
        with _lock:
            result = func(*args, **kwargs)
        return result

    return wrapper
