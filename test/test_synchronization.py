# -*- coding: utf-8 -*-
"""
Synchronization tests, using py.test. Run as:

$ easy_install -U py
$ py.test
"""
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
