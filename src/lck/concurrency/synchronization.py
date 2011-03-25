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

"""lck.concurrency.synchronization
   -------------------------------

   Implements a reusable Java-like synchronization decorator.
   It is using threading locks or filesystem-based locks to synchronize
   subsequent calls of the specified functions. The former kind of
   lock is reentrant, the latter is not.

   For filesystem-based locks the module is using Skip Montanaro's
   `lockfile <http://pypi.python.org/pypi/lockfile>`_ library,
   compatible with Windows and POSIX environments."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
from threading import RLock
from lockfile import FileLock
from functools import wraps

def synchronized(func=None, lock=None, path=None):
    """ Synchronization decorator.

        :param lock: the user can specify a concrete lock object to be used
               with this specific synchronization decorator. This is
               useful when a group of functions should be synchronized
               together.
        :param path: instead of using threading-based locking, file-based
               locks may be used instead. Beware, these are radically
               less performant than threading locks.
    """

    # the decarator can be used with an argument as well as without any
    if func is None:
        def wrapper(f):
            return synchronized(f, lock=lock)
        return wrapper

    if path is None:
        _lock = lock if lock else RLock()
    else:
        _lock = FileLock(path)

    @wraps(func)
    def wrapper(*args, **kwargs):
        with _lock:
            result = func(*args, **kwargs)
        return result

    return wrapper
