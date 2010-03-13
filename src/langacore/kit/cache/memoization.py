# -*- coding: utf-8 -*-
"""
A reusable memoization decorator implementation. It is using a cache of pickled arguments
"""
 
import cPickle as pickle
import sys
from time import time
from functools import wraps
 

DEFAULT_MEMOIZE_MAX_SIZE=256

 
def memoize(func=None, update_interval=300, max_size=DEFAULT_MEMOIZE_MAX_SIZE, skip_first=False):
    """ memoization decorator. 
    
        update_interval - time in seconds after which the actual function will be called again 
        max_size - maximum buffer count for distinct memoize hashes for the function 
        skip_first - if True, the first argument to the actual function won't be added to the memoize hash 
    """

    # the decarator can be used with an argument as well as without any 
    if func is None:
        def wrapper(f):
            return memoize(f, update_interval=update_interval, max_size=max_size, skip_first=skip_first)
        return wrapper
 
    cached_values = {}
    lru_list = []
 
    @wraps(func)
    def wrapper(*args, **kwargs):
        if skip_first:
            key = pickle.dumps((args[1:], kwargs))
        else:
            key = pickle.dumps((args, kwargs))
 
        if key in cached_values:
            # move argument to the end of the LRU list
            lru_list.append(lru_list.pop(lru_list.index(key)))
            
            # get the buffered values and check whether they are up-to-date
            result, acquisition_time = cached_values[key]
            if time() - acquisition_time > update_interval:
                del cached_values[key]

        if key not in cached_values:
            cached_values[key] = (func(*args, **kwargs), time())
            lru_list.append(key)   
 
            # clear the least recently used value if the maximum size 
            # of the buffer is exceeded
            if max_size is not None and len(lru_list) > max_size:
                del cached_values[lru_list.pop(0)]

        return cached_values[key][0]
 
    return wrapper
