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

"""lck.config
   ----------

   Configuration related utilities."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import Callable

from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError


class FunkyConfigParser(SafeConfigParser):
    """Config parser that can handle get() fallbacks and getting/setting lists
    of strings (white-space separated)."""

    def __init__(self, *args, **kwargs):
        self.is_fresh = True
        SafeConfigParser.__init__(self, *args, **kwargs)

    def readfp(self, *args, **kwargs):
        self.is_fresh = False
        SafeConfigParser.readfp(self, *args, **kwargs)

    def write(self, *args, **kwargs):
        self.is_fresh = False
        SafeConfigParser.write(self, *args, **kwargs)

    def set(self, section, option, value):
        if isinstance(value, list):
            SafeConfigParser.set(self, section, option, " ".join(value))
        else:
            SafeConfigParser.set(self, section, option, str(value))

    def get(self, section, option, fallback=None, conv=str):
        try:
            raw_value = SafeConfigParser.get(self, section, option)
        except (NoOptionError, NoSectionError):
            if fallback is None:
                raise
            elif isinstance(fallback, Callable):
                return fallback(section, option)
            else:
                return fallback
        if conv == list:
            return raw_value.strip().split()
        elif conv == bool:
            if raw_value.lower() not in self._boolean_states:
                raise ValueError('Not a boolean: %s' % raw_value)
            return self._boolean_states[raw_value.lower()]
        else:
            return conv(raw_value)

    def getint(self, section, option, fallback=None):
        return self.get(section, option, fallback, int)

    def getfloat(self, section, option, fallback=None):
        return self.get(section, option, fallback, float)

    def getlist(self, section, option, fallback=None):
        return self.get(section, option, fallback, list)

    def getboolean(self, section, option, fallback=None):
        return self.get(section, option, fallback, bool)
