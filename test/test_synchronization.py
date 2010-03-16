# -*- coding: utf-8 -*-
"""
Synchronization tests, using py.test. Run as:

$ easy_install -U py
$ py.test
"""
from threading import Thread, Lock, RLock
from time import time, sleep

from langacore.kit.concurrency import synchronized


def test_simple_synchronization():
    @synchronized
    def simple_synchro(result):
        for i in xrange(10):
            result.append(i)
            sleep(0.1)
    
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


def test_shared_synchronization():
    lock = Lock()
    
    class SharedLockThread(Thread):
        def __init__(self, result):
            Thread.__init__(self)
            self.result = result

        @synchronized(lock=lock) 
        def run(self):
            for i in xrange(10):
                self.result.append(i)
                sleep(0.1)

    result = []
    threads = [SharedLockThread(result) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert result == range(10) * 10


def test_reentrant_synchronization():
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
            sleep(0.1)
            self.run(i + 1)

    result = []
    threads = [ReentrantThread(result) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert result == range(10) * 10
