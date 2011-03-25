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

"""lck.files.finder
   ----------------

   Provides a function for searching for a file in sensible locations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os


class CommonPathPrefixes(list):
    def __init__(self):
        """Instantiates common path prefixes used in search for specific file.
           For now these are: the current and parent directory, subdirectories
           of the current directory, possible home directories for the current
           user.

           ..note::
             We don't check the __file__ directory of any module because we
             believe data should not be mixed with code."""
        self.append('.')
        self.append('..')
        for entry in os.listdir('.'):
            if not os.path.isdir(entry):
                continue
            self.append(os.path.join('.', entry))
        if 'HOME' in os.environ:
            self.append(os.environ['HOME'])
        elif 'USER' in os.environ:
            self.append('/home/{USER}'.format(os.environ))
            self.append('/home/users/{USER}'.format(os.environ))
            self.append('/Users/{USER}'.format(os.environ))
        self.append('/etc')

    def generate(self, *args):
        """Returns a generator that yields existing paths for every permutation
           of the common path prefixes with paths in the specified list. Paths
           are permuted only when the one from the given list is not
           absolute."""

        for p in args:
            if not p:
                continue
            elif os.path.isabs(p):
                if os.path.exists(p):
                    yield p
                continue
            for prefix in self:
                generated_path = os.path.join(prefix, p)
                if os.path.exists(generated_path):
                    yield generated_path

common_path_prefixes = CommonPathPrefixes()

def finder(explicit_path, envvar=None, multiple_allowed=False):
    """Finds a specific file using explicitly given path (or given by an
       environment variable). The algorithm is as follows: for every given
       path from the args (explicitly given, environment variable, fallback)
       check whether the file exists. If it doesn't and the path is not
       absolute, search the working directory, its parent directory and all
       child directories, the current user's home directory and /etc.

       :param explicit_path: path explicitly given by the user, can be a single
                             entry or a sequence

       :param envvar: name of the environment variable where to look for the
                      path

       :param fallback: name of the file to check if everything else fails

       :param multiple_allowed: False by default. If True, the returned type is
                                a tuple with potentially many entries.

       :return: the real absolute path to the file. Raises IOError if no found.

       ..note::
         Works only on POSIX systems."""

    if not explicit_path:
        explicit_path = []
    elif explicit_path.__class__ in (list, tuple, set):
        # list copying for safety reasons (routine is side-effect free)
        explicit_path = list(explicit_path)
    else:
        explicit_path = [explicit_path]

    explicit_path.append(os.environ.get(envvar))

    # keep only given arguments
    existing_paths = common_path_prefixes.generate(*explicit_path)

    try:
        if multiple_allowed:
            existing_paths = list(existing_paths)
            if not existing_paths:
                raise StopIteration()
            return existing_paths
        else:
            return existing_paths.next()
    except StopIteration:
        raise IOError("File not found.")
