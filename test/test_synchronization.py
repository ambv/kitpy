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

"""Synchronization tests
   ---------------------

   Tests use the ``py.test`` framework. Run as::

       $ easy_install -U py
       $ py.test
   """

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from threading import Thread, Lock, RLock
from time import time, sleep

from lck.concurrency import synchronized

SLEEP_AMOUNT=0.05 #seconds

def test_simple_synchronization(sleep_amount=SLEEP_AMOUNT):
    @synchronized
    def simple_synchro(result):
        for i in xrange(10):
            result.append(i)
            sleep(sleep_amount)

    class SimpleThread(Thread):
        def __init__(self, result):
            Thread.__init__(self)
            self.result = result
        def run(self):
            simple_synchro(self.result)

    result = []
    threads = [SimpleThread(result) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert result == range(10) * 10


def test_shared_synchronization(sleep_amount=SLEEP_AMOUNT):
    lock = Lock()

    class SharedLockThread(Thread):
        def __init__(self, result):
            Thread.__init__(self)
            self.result = result

        @synchronized(lock=lock)
        def run(self):
            for i in xrange(10):
                self.result.append(i)
                sleep(sleep_amount)

    result = []
    threads = [SharedLockThread(result) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert result == range(10) * 10


def test_reentrant_synchronization(sleep_amount=SLEEP_AMOUNT):
    lock = RLock()

    class ReentrantThread(Thread):
        def __init__(self, result):
            Thread.__init__(self)
            self.result = result

        @synchronized(lock=lock)
        def run(self, i=0):
            if i > 9:
                return

            self.result.append(i)
            sleep(sleep_amount)
            self.run(i + 1)

    result = []
    threads = [ReentrantThread(result) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert result == range(10) * 10


def test_filebased_synchronization(sleep_amount=SLEEP_AMOUNT):
    class FilesystemLockThread(Thread):
        def __init__(self, result):
            Thread.__init__(self)
            self.result = result

        @synchronized(path='./test.lock')
        def run(self):
            for i in xrange(10):
                self.result.append(i)
                sleep(sleep_amount)

    result = []
    threads = [FilesystemLockThread(result) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert result == range(10) * 10
