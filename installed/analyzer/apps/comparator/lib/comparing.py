#!/usr/bin/python2.6
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

"""library to compare the fingerprints of the document with the fingerprint database
"""

__authors__ = [
    '"Kailash Budhathoki" <kailash.buki@gmail.com>'
]


from gevent_zeromq import zmq
import json
import logging
from operator import itemgetter

from pymongo import Connection


def _create_db_handler():
    """Creates a pymongo db handler
    
    Args: None
    
    Returns: None
    """
    connection = Connection()
    return connection['predator']

def compare(fingerprints):
    """Compares the fingerprints with the fingerprint database
    
    Args:
        fingerprints: list of fingerprints of the document
        
    Returns:
        per_match: percentile match with documents in the db    
    """
    db = _create_db_handler()
    num_fp = len(fingerprints)
    per_match = {}
    total_match = fp_found = 0
    
    for fp in fingerprints:
        result = db.fingerprint.find_one({'fingerprint': fp[0]})
        if result:
            fp_found += 1
            docs = result['doc_info']
            for doc in docs:
                per_match[doc] = per_match[doc] + 1 if per_match.get(doc) else 1
                                               
    if per_match:                     
        for doc, count in per_match.iteritems():
            per_match[doc] = (count * 1.0 / num_fp) * 100
        
        per_match = sorted(per_match.iteritems(), key=itemgetter(1), reverse=True)    
        total_match = (fp_found * 1.0 / num_fp) * 100
    
    match = dict(total_match = total_match, per_match = per_match)
    
    return match


