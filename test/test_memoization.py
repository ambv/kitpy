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
