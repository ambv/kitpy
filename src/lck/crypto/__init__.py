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

"""lck.crypto
   ----------

   High-level cryptographic routines."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from functools import partial

from Crypto.Cipher import AES as _AES
from Crypto.Cipher import Blowfish as _Blowfish
from Crypto.Cipher import CAST as _CAST
from Crypto.Cipher import DES as _DES
from Crypto.Cipher import DES3 as _DES3

from .cipher import Cipher

def _setup_cipher(cipher):
    part = partial(Cipher, cipher=cipher)
    name = cipher.__name__.split('.')[-1]
    part.__name__ = name.lower()
    part.__module__ = b'lck.crypto.cipher'
    part.__doc__ = ("{}([key, path, create]) -> Cipher instance\n\nFactory "
        "creating a cipher using the {} algorithm. Arguments have the same "
        "meaning as in the raw Cipher class.").format(part.__name__, name)
    # FIXME: how do I make this work with >>> help(part) ???
    return part

aes = _setup_cipher(_AES)
blowfish = _setup_cipher(_Blowfish)
cast = _setup_cipher(_CAST)
des = _setup_cipher(_DES)
des3 = _setup_cipher(_DES3)
