#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Łukasz Langa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""langacore.kit.concurrency.synchronization
   -----------------------------------------

   Implements a reusable Java-like synchronization decorator.
   It is using threading locks or filesystem-based locks to synchronize
   subsequent calls of the specified functions. The former kind of
   lock is reentrant, the latter is not.

   For filesystem-based locks the module is using Skip Montanaro's
   `lockfile <http://pypi.python.org/pypi/lockfile>`_ library,
   compatible with Windows and POSIX environments."""

from __future__ import absolute_import
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
