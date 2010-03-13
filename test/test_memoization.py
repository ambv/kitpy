# -*- coding: utf-8 -*-
"""
Memoization tests, using py.test. Run as:

$ easy_install -U py
$ py.test
"""
from time import time, sleep

from langacore.kit.cache import memoize


def test_memoization_update_interval():
    @memoize(update_interval=4)
    def current_time():
        return time()

    t = current_time()
    sleep(1)
    assert t == current_time()
    sleep(1)
    assert t == current_time()
    sleep(3)
    assert t != current_time()


def test_memoization_max_size():
    @memoize(max_size=2)
    def current_time(arg):
        return time()

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
