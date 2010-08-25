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

"""langacore.kit.config
   --------------------

   Configuration related utilities."""

from __future__ import absolute_import
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
