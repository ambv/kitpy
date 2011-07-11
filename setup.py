# -*- encoding: utf-8 -*-
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

import os
import sys
from setuptools import setup, find_packages

assert sys.version_info >= (2, 7), "Python 2.7+ required."

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as ld_file:
    long_description = ld_file.read()

from doc.conf import release

setup (
    name = 'lck.common',
    version = release,
    author = 'Lukasz Langa',
    author_email = 'lukasz@langa.pl',
    description = ("A library of various simple common routines that keep "
                   "being rewritten all over again in every project I'm "
                   "working on."),
    long_description = long_description,
    url = 'http://packages.python.org/lck.common/',
    keywords = '',
    platforms = ['any'],
    license = 'MIT',
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['lck'],
    zip_safe = True,
    install_requires = [
        'lockfile',
        'null',
        'pycrypto',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows NT/2000',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
