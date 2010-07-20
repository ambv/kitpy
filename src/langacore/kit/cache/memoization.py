# -*- coding: utf-8 -*-
"""\
Implements a reusable memoization decorator. It is using a finite-size cache
with pickled arguments as keys, to hold the outcome of a specific function call.
When the decorated function is called again with the same arguments, the outcome
is fetched from the cache instead of being recalculated again.

The cache used maintains a list of *Least Recently Used* keys so that in case of
overflow only the seemingly least important ones get deleted.
"""
 
import cPickle as pickle
import sys
from time import time
from functools import wraps
 

def memoize(func=None, update_interval=300, max_size=256, skip_first=False, fast_updates=False):
    """Memoization decorator.
            
        :param update_interval: time in seconds after which the actual function will be called again 
        :param max_size: maximum buffer count for distinct memoize hashes for the function 
        :param skip_first: ``False`` by default; if ``True``, the first argument to the actual
                            function won't be added to the memoize hash 
        :param fast_updates: ``False`` by default; if ``True``, an alternative LRU algorithm is used
                             where all function invocations except every Nth (where N == sys.maxint)
                             are much faster but cache overflow is costly. In general, set 
                             ``fast_updates`` to ``True`` for functions where you are sure that the
                             possible number of argument combinations is smaller than ``max_size``
    """

    # the decorator can be used with an argument as well as without any 
    if func is None:
        def wrapper(f):
            return memoize(func=f,
                           update_interval=update_interval,
                           max_size=max_size,
                           skip_first=skip_first,
                           fast_updates=fast_updates)
        return wrapper
 
    cached_values = {}

    if fast_updates:
        lru_indices = {'CURRENT': 0}
    else: 
        lru_list = []
 
    @wraps(func)
    def wrapper_standard(*args, **kwargs):
        if skip_first:
            key = pickle.dumps((args[1:], kwargs))
        else:
            key = pickle.dumps((args, kwargs))
 
        if key in cached_values:
            # move argument to the end of the LRU list
            lru_list.append(lru_list.pop(lru_list.index(key)))
            
            # get the buffered values and check whether they are up-to-date
            result, acquisition_time = cached_values[key]
            if update_interval and time() - acquisition_time > update_interval:
                del cached_values[key]

        if key not in cached_values:
            cached_values[key] = (func(*args, **kwargs), time())
            lru_list.append(key)   
 
            # clear the least recently used value if the maximum size 
            # of the buffer is exceeded
            if max_size is not None and len(lru_list) > max_size:
                del cached_values[lru_list.pop(0)]

        return cached_values[key][0]
    
    @wraps(func)
    def wrapper_fast_updates(*args, **kwargs):
        if skip_first:
            key = pickle.dumps((args[1:], kwargs))
        else:
            key = pickle.dumps((args, kwargs))

        lru_indices['CURRENT'] += 1
        lru_indices[key] = lru_indices['CURRENT']
 
        if key in cached_values:
            # get the buffered values and check whether they are up-to-date
            result, acquisition_time = cached_values[key]
            if update_interval and time() - acquisition_time > update_interval:
                del cached_values[key]

        if key not in cached_values:
            cached_values[key] = (func(*args, **kwargs), time())
 
            # clear the least recently used value if the maximum size 
            # of the buffer is exceeded
            if max_size is not None and len(lru_indices) > max_size:
                lru_key = min(lru_indices.iteritems(), key=lambda x: x[1])[0]         
                del lru_indices[lru_key]
                del cached_values[lru_key]

        if lru_indices['CURRENT'] == sys.maxint:
            # renumber indices to avoid hurting performance by using bigints
            lru_indices['CURRENT'] = 0
            for key, _ in sorted(lru_indices.iteritems(), key=lambda x: x[1]):
                lru_indices[key] = lru_indices['CURRENT']
                lru_indices['CURRENT'] += 1

        return cached_values[key][0]
 
    return wrapper_standard if not fast_updates else wrapper_fast_updates
