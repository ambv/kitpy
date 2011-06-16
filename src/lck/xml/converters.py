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

from lck.lang import null

class nulldict(dict):
    def __missing__(self, key):
        return null

def _datetime(value):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

def _datetime_strip_tz(value):
    return datetime.strptime(value[:-6], '%Y-%m-%dT%H:%M:%S')

_converters = [int, float, _datetime, _datetime_strip_tz]

def etree_to_dict(element, namespace=""):
    """etree_to_dict(element, [namespace]) -> ("tag_name", dict_with_children)

    `element` must be a valid ElementTree element. `namespace` is optional,
    must be given in Clark notation, e.g. "{ns_uri}".
    """
    if namespace and not element.tag.startswith(namespace):
        return None, None
    if len(element):
        response = nulldict()
        for sub_element in element:
            tag, value = etree_to_dict(sub_element, namespace=namespace)
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
