#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 by Łukasz Langa
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""lck.cache.memoization
   ---------------------

   Implements a reusable memoization decorator. It is using a finite-size cache
   with pickled arguments as keys, to hold the outcome of a specific function
   call. When the decorated function is called again with the same arguments,
   the outcome is fetched from the cache instead of being recalculated again.

   The cache used maintains a list of *Least Recently Used* keys so that in
   case of overflow only the seemingly least important ones get deleted.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import cPickle as pickle
import sys
from time import time
from functools import wraps


def memoize(func=None, update_interval=300, max_size=256, skip_first=False,
    fast_updates=True):
    """Memoization decorator.

        :param update_interval: time in seconds after which the actual function
                                will be called again

        :param max_size: maximum buffer count for distinct memoize hashes for
                         the function. Can be set to 0 or ``None``. Be aware of
                         the possibly inordinate memory usage in that case

        :param skip_first: ``False`` by default; if ``True``, the first
                           argument to the actual function won't be added to
                           the memoize hash

        :param fast_updates: if ``True`` (the default), an optimized LRU
                             algorithm is used where all function invocations
                             except every Nth (where N == sys.maxint) are much
                             faster but cache overflow is costly. In general,
                             having ``fast_updates`` set to ``True`` gives
                             a 15% performance boost when there are no cache
                             misses (the possible number of used argument
                             combinations for the decorated function is smaller
                             than the value of ``max_size``). If cache misses
                             exceed 50%, you might want to increase
                             ``max_size``. If that's not feasible, memoization
                             with ``fast_updates`` set to ``False`` will
                             perform faster."""

    # the decorator can be used with an argument as well as without any
    if func is None:
        def wrapper(f):
            return memoize(func=f,
                           update_interval=update_interval,
                           max_size=max_size,
                           skip_first=skip_first,
                           fast_updates=fast_updates)
        return wrapper

    if fast_updates:
        cached_values = {'MAX_INDEX': 0}
        lru_indices = {}
    else:
        cached_values = {}
        lru_list = []

    @wraps(func)
    def wrapper_standard(*args, **kwargs):
        if skip_first:
            key = pickle.dumps((args[1:], kwargs))
        else:
            key = pickle.dumps((args, kwargs))

        max_index = cached_values['MAX_INDEX'] + 1
        lru_indices[key] = max_index

        if key in cached_values:
            # get the buffered values and check whether they are up-to-date
            result, acquisition_time = cached_values[key]
            if update_interval and time() - acquisition_time > update_interval:
                del cached_values[key]

        if key not in cached_values:
            try:
                result = func(*args, **kwargs)
            except:
                del lru_indices[key]
                raise
            acquisition_time = time()
            cached_values[key] = (result, acquisition_time)

            # clear the least recently used value if the maximum size
            # of the buffer is exceeded
            if max_size and len(lru_indices) > max_size:
                lru_key, _ = min(lru_indices.iteritems(), key=lambda x: x[1])
                del lru_indices[lru_key]
                del cached_values[lru_key]

        if max_index == sys.maxint:
            # renumber indices to avoid hurting performance by using bigints
            max_index = 0
            for key, _ in sorted(lru_indices.iteritems(), key=lambda x: x[1]):
                lru_indices[key] = max_index
                max_index += 1

        cached_values['MAX_INDEX'] = max_index

        return result

    @wraps(func)
    def wrapper_legacy(*args, **kwargs):
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
                lru_list.remove(key)

        if key not in cached_values:
            cached_values[key] = (func(*args, **kwargs), time())
            lru_list.append(key)

            # clear the least recently used value if the maximum size
            # of the buffer is exceeded
            if max_size and len(lru_list) > max_size:
                del cached_values[lru_list.pop(0)]

        return cached_values[key][0]

    return wrapper_standard if fast_updates else wrapper_legacy
