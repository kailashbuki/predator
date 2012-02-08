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

"""library to listen to the incoming requests and publish the result to the
other engine
"""

__authors__ = [
    '"Kailash Budhathoki" <kailash.buki@gmail.com>'
]


import gevent
from gevent_zeromq import zmq
import json
import logging
import os
import sys

from keeper import save_fp, archive_text_file
PREDATOR_HOME = os.environ['PREDATOR_HOME']
sys.path.append(PREDATOR_HOME)
from libfp.generating import FingerprintGenerator


def _create_fpkeeper_in():
    """zmq socket is created for incoming requests. Incoming requests come from
    pdf2textconverter app
    
    Args: None
    
    Returns: 
        A zmq socket for listening incoming requests
    """
    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.PULL)
    zmq_socket.connect('tcp://127.0.0.1:9004')
    
    return zmq_socket

def _create_fpkeeper_out():
    """zmq socket is created for publishing messages
    
    Args: None
    
    Returns: 
        A zmq socket for dispatching results
    """
    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.PUSH)
    zmq_socket.bind('tcp://127.0.0.1:9005')    
    return zmq_socket    

def _process_request(fpkeeper_out, request):
    """processes incoming requests to fpkeeper in a separate
    greenlet
    
    Args:
        fpkeeper_out: dispatching zmq socket
        request: request parameter
    
    Returns: None
    """
    standard_string = request.get('standard_string')
    text_path = request.get('text_path')
    do_what = request.get('do_what')
    identity = request.get('identity')
    
    if 'standard_string' in request and 'text_path' in request and 'do_what' in \
                                                request and 'identity' in request:
        fpg = FingerprintGenerator(input_string=standard_string)
        fpg.generate_fingerprints()
        fingerprints = fpg.fingerprints

        if do_what == 'archive':
            logging.warn('FPKEEPER: Archiving the text file into the file system ...')
            archived_path = archive_text_file(text_path)
            logging.warn('FPKEEPER: Saving the fingerprints into the database ...')
            
            for fingerprint in fingerprints:
                save_fp(fingerprint[0], archived_path)
            
            logging.warn('FPKEEPER: Document fingerprints were saved into the db.')
            
        elif do_what == 'check':

            logging.warn('FPKEEPER: Dispatching the fingerprints to the analyzer engine.')
            fpkeeper_out.send_json(dict(fingerprints=fingerprints, identity=identity))
            
    else:
        logging.warn('FPKEEPER: Unknown parameters in the request to fpkeeper.')


def listener_loop_runner():
    """Runs the loop to listen to the incoming requests and dispatch the task to
    another engine
    
    Args:
        None
    
    Returns: None
    """
    fpkeeper_in = _create_fpkeeper_in()
    fpkeeper_out = _create_fpkeeper_out()

    while True:
        request = fpkeeper_in.recv_json()
        logging.warn('FPKEEPER: Received request ...')
        
        gevent.spawn_link_exception(_process_request, fpkeeper_out, request) 
        