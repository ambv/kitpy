# -*- coding: utf-8 -*-
"""
A reusable synchronization decorator implementation. It is using 
threading locks or filesystem-based locks to synchronize
subsequent calls of the specified functions. The former kind of
lock is reentrant, the latter is not.

For filesystem-based locks the module is using Skip Montanaro's
``lockfile`` library, compatible with Windows and POSIX environments.
"""
from __future__ import with_statement

import sys
from threading import RLock
from lockfile import FileLock
from functools import wraps
 

def synchronized(func=None, lock=None, path=None):
    """ synchronization decorator. 
    
        lock - the user can specify a concrete lock object to be used 
               with this specific synchronization decorator. This is 
               useful when a group of functions should be synchronized
               together.
        path - instead of using threading-based locking, file-based
               locks may be used instead. Beware, these are radically
               less performant than threading locks.
    """

    # the decarator can be used with an argument as well as without any 
    if func is None:
        def wrapper(f):
            return synchronized(f, lock=lock)
        return wrapper
 
    # threading lock
    if path is None:
        _lock = lock if lock else RLock()

        @wraps(func)
        def wrapper(*args, **kwargs):
            with _lock:
                result = func(*args, **kwargs)
            return result
    # file-based lock
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            _lock = FileLock(path)
            while not _lock.is_locked():
                _lock.acquire()
            result = func(*args, **kwargs)
            _lock.release()
            return result
    
    return wrapper
