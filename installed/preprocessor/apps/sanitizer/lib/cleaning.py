#!/usr/bin/env python
#
# Copyright (C) 2011 by kailash.buki@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""library to read the text file and sanitize the text
"""

__authors__ = [
    '"Kailash Budhathoki" <kailash.buki@gmail.com>'
]


def sanitize(path):
    """Reads the text file from the path and sanitizes the raw string. That
    standard string is fed to the fingerprinting component.
    
    Args:
        path: An absolute file path of the text file
        
    Returns:
        The standard string as per the predator requirement
    """
    with open(path, 'r') as stream:
        raw_text = unicode(stream.read(), errors='ignore')
        lowered_text = raw_text.lower()
        standard_text = ''.join([c for c in lowered_text if c not in (' ', '\r', '\n')])
        return standard_text


if __name__ == '__main__':
    print sanitize('/Users/sagardh/Documents/Kernighan_Ritchie_Language_C.txt')
