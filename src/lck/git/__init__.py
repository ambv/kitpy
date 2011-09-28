#!/usr/bin/env python
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

"""lck.git
   -------

   Helpers for git repositories."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import shlex
import subprocess

from lck.cache import memoize


def get_version(module):
    """
    get_version(module) -> u'git-shortSHA1 (date & time of last commit)'

    Returns a short, nicely formatted tag that can be used for versioning
    purposes on websites or command-line tools. The version given is based
    on the last commit on the repository the specified `module` object is
    a part of.
    """
    if isinstance(module, basestring):
        return _get_version(module)
    else:
        return _get_version(os.path.split(module.__file__)[0])

@memoize
def _get_version(path):
    try:
        out = subprocess.check_output(
            shlex.split(b'git log --pretty=format:"git-%h (%ad)" --date=iso'),
            cwd=path, stderr=subprocess.STDOUT)
        return out.split('\n')[0]
    except (OSError, subprocess.CalledProcessError):
        return None
