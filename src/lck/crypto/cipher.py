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

"""lck.crypto.cipher
   -----------------

   Based on http://code.activestate.com/recipes/496763/."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from base64 import b64encode, b64decode
import os
import random
import stat
import string
import tempfile

from lck.concurrency import synchronized

ALPHABET = string.letters + string.digits + string.punctuation


class Cipher(object):
    def __init__(self, key=None, path=None, create=True, cipher=None):
        """Using a provided `key` or `path` to a file with the key, create
        a Cipher capable of encrypting and decrypting bytes. `cipher` is
        the algorithm to be used.

        If `path` is provided and `create` is True, if the file under `path`
        is absent, it is created."""

        if key is None:
            if path is None:
                raise ValueError('Either `key` or `path` must be provided.')
            length = 32 if not cipher.key_size else cipher.key_size
            key = self.key_from_path(path, create, length)
        self._cipher = cipher.new(key)
        self.block = self._cipher.block_size

    @staticmethod
    @synchronized(path=os.path.join(tempfile.gettempdir(),
        'lck-crypto-cipher.lock'))
    def key_from_path(path, create=True, length=32):
        if not os.path.exists(path):
            if not create:
                raise IOError("File does not exist: {}".format(path))
            else:
                with open(path, "wb") as key_file:
                    key_file.write(''.join([random.choice(ALPHABET)
                        for i in range(length)]))
                    key_file.flush()
                    os.fchmod(key_file.fileno(), stat.S_IRUSR)
        with open(path, "rb") as key_file:
            return key_file.read()

    def encrypt(self, buffer, base64=False):
        """Encrypts the specified ``buffer``, optionally encoding the result to
        Base64.

        Note: only bytestrings can be encrypted directly. For Unicode strings,
        encode them to bytes first."""
        assert isinstance(buffer, bytes), "Cannot encrypt {} instances. "\
            "Encode to bytes first.".format(buffer.__class__.__name__)
        result = self._cipher.encrypt(self._pad_buffer(buffer))
        if base64:
            result = b64encode(result)
        return result

    def decrypt(self, buffer, base64=False):
        """Descrypt the specified ``buffer``, optionally decoding from Base64
        first.

        Note: only bytestrings can be decrypted directly. For Unicode strings,
        encode them to bytes first."""
        assert isinstance(buffer, bytes), "Cannot decrypt {} instances. "\
            "Encode to bytes first.".format(buffer.__class__.__name__)
        if base64:
            buffer = b64decode(buffer)
        result = self._depad_buffer(self._cipher.decrypt(buffer))
        return result

    # the cipher needs self.block byte blocks to work with
    def _pad_buffer(self, buffer):
        pad_bytes = self.block - (len(buffer) % self.block)
        for i in range(pad_bytes - 1):
            buffer += chr(random.randrange(0, 256))
        # final padding byte; % by self.block to get the number of padding bytes
        bflag = random.randrange(6, 256 - self.block)
        bflag -= bflag % self.block - pad_bytes
        buffer += chr(bflag)
        return buffer

    def _depad_buffer(self, buffer):
        pad_bytes = ord(buffer[-1]) % self.block
        if not pad_bytes:
            pad_bytes = self.block
        return buffer[:-pad_bytes]
