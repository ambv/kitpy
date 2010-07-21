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

from langacore.kit.concurrency import synchronized

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
