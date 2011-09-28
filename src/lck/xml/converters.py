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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from functools import partial
from htmlentitydefs import name2codepoint as n2cp
import re

ENTITY_REGEX = re.compile(r'&(#?)(x?)(\d{1,5}|\w{1,8});')

def _datetime(value):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

def _datetime_strip_tz(value):
    return datetime.strptime(value[:-6], '%Y-%m-%dT%H:%M:%S')

_converters = [int, float, _datetime, _datetime_strip_tz]

def etree_to_dict(element, namespace="", _converters=_converters):
    """etree_to_dict(element, [namespace]) -> ("tag_name", dict_with_children)

    `element` must be a valid ElementTree element. `namespace` is optional,
    must be given in Clark notation, e.g. "{ns_uri}".
    """
    if namespace and not element.tag.startswith(namespace):
        return None, None
    if len(element):
        response = {}
        for sub_element in element:
            tag, value = etree_to_dict(sub_element, namespace=namespace,
                _converters=_converters)
            if not tag:
                continue
            if tag in response:
                if isinstance(response[tag], list):
                    response[tag].append(value)
                else:
                    response[tag] = [response[tag], value]
            else:
                response[tag] = value
    else:
        response = element.text
        for converter in _converters:
            try:
                response = converter(response)
            except (ValueError, TypeError):
                continue
            else:
                break
    return element.tag[len(namespace):], response

def substitute_entity(match):
    ent = match.group(3)

    if match.group(1) == "#":
        if match.group(2) == '':
            return unichr(int(ent))
        elif match.group(2) == 'x':
            return unichr(int('0x'+ent, 16))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def substitute_entity_encode(match, encoding):
    result = substitute_entity(match)
    if isinstance(result, unicode):
        result = result.encode(encoding)
    return result

def decode_entities(string, encoding=None):
    """decode_entities(string, [encoding]) -> string_with_decoded_entities

    Decodes XML entities from the given string. Supports both Unicode and
    bytestring arguments.

    Note: when using a bytestring `string` argument, a bytestring will be
    returned. In that case however, `encoding` has to be specified, otherwise
    an UnicodeDecodeError will be raised. This is because we have to support
    the &#xxxx; entity which enables people to use any Unicode codepoint.
    """
    substitute = substitute_entity
    if encoding:
        substitute = partial(substitute_entity_encode,
            encoding=encoding)
    return ENTITY_REGEX.subn(substitute, string)[0]
