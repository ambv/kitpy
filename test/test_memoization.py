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

"""Memoization tests
   -----------------

   Tests use the ``py.test`` framework. Run as::

       $ easy_install -U py
       $ py.test
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from time import time, sleep

from lck.cache import memoize

def _update_interval_test(current_time):
    t = current_time()
    sleep(1)
    assert t == current_time()
    sleep(1)
    assert t == current_time()
    sleep(3)
    assert t != current_time()

def _max_size_test(current_time):
    t1 = current_time(1)
    sleep(1)
    t2 = current_time(2)

    sleep(1)
    assert t1 == current_time(1)
    assert t2 == current_time(2)

    t3 = current_time(3)
    sleep(1)
    t4 = current_time(4)

    sleep(1)
    assert t3 == current_time(3)
    assert t4 == current_time(4)
    assert t1 != current_time(1)
    assert t2 != current_time(2)

    sleep(1)
    assert t3 != current_time(3)
    assert t4 != current_time(4)

def _exception_test(current_time):
    t1 = current_time(1)
    sleep(1)
    t2 = current_time(2)

    sleep(1)
    assert t1 == current_time(1)
    assert t2 == current_time(2)

    sleep(1)
    try:
        t0 = current_time(1)
    except ValueError:
        pass
    else:
        assert False, "Exception not raised ({}).".format("stale value"
            if t1 == t0 else "new value")

    t3 = current_time(3)
    t4 = current_time(4)

    sleep(1)
    assert t3 == current_time(3)
    assert t4 == current_time(4)

def test_memoization_update_interval():
    @memoize(fast_updates=False, update_interval=4)
    def current_time():
        return time()
    _update_interval_test(current_time)

def test_memoization_max_size():
    @memoize(fast_updates=False, max_size=2)
    def current_time(arg):
        return time()
    _max_size_test(current_time)

def test_memoization_exception():
    already_used = set()
    @memoize(fast_updates=False, update_interval=3, max_size=2)
    def current_time(arg):
        if arg in already_used:
            raise ValueError('argument already used')
        already_used.add(arg)
        return time()
    _exception_test(current_time)

def test_memoization_fast_updates_update_interval():
    @memoize(fast_updates=True, update_interval=4)
    def current_time():
        return time()
    _update_interval_test(current_time)

def test_memoization_fast_updates_max_size():
    @memoize(fast_updates=True, max_size=2)
    def current_time(arg):
        return time()
    _max_size_test(current_time)

def test_memoization_fast_updates_exception():
    already_used = set()
    @memoize(fast_updates=True, update_interval=3, max_size=2)
    def current_time(arg):
        if arg in already_used:
            raise ValueError('argument already used')
        already_used.add(arg)
        return time()
    _exception_test(current_time)
