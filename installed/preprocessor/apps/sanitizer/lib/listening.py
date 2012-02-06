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

from cleaning import sanitize



def _create_sanitizer_in():
    """zmq socket is created for incoming requests. Incoming requests come from
    pdf2textconverter app
    
    Args: None
    
    Returns: 
        A zmq socket for listening incoming requests
    """
    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.PULL)
    zmq_socket.connect('tcp://127.0.0.1:9003')
    
    return zmq_socket

def _create_sanitizer_out():
    """zmq socket is created for publishing messages
    
    Args: None
    
    Returns: 
        A zmq socket for dispatching results
    """
    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.PUSH)
    zmq_socket.bind('tcp://127.0.0.1:9004')

    
    return zmq_socket    

def _process_request(sanitizer_out, request):
    """processes request coming to the sanitizer in a 
    separate greenlet
    Args:
        sanitizer_out: outgoing zmq socket
        request: request parameters
    """
    standard_string = request.get('standard_string')
    text_path = request.get('text_path')
    do_what = request.get('do_what')
    identity = request.get('identity')
    
    if 'text_path' in request and 'do_what' in request and 'identity' in request:
        try:
            logging.warn('SANITIZER: Sanitizing text')
            standard_string = sanitize(text_path)
            logging.warn('SANITIZER: Standard string produced, now dispatching it to the storekeeper ...')
            sanitizer_out.send_json(dict(standard_string = standard_string,
                                         text_path = text_path, 
                                         do_what = do_what,
                                         identity = identity))
        except IOError:
            logging.warn('SANITIZER: Text file path %s was not found.' % text_path)
    else:
        logging.warn('SANITIZER: Unknown parameters in the request to sanitizer.')

def listener_loop_runner():
    """Runs the loop to listen to the incoming requests and dispatch the task to
    another engine
    
    Args:
        None
    
    Returns: None
    """
    # TODO (kailash.buki@gmail.com): forward all errors to the alert engine
    sanitizer_in = _create_sanitizer_in()
    sanitizer_out = _create_sanitizer_out()
    
    while True:
        request = sanitizer_in.recv_json()
        logging.warn('SANITIZER: Received request ...')
        logging.warn('           %s' % request)

        gevent.spawn_link_exception(_process_request, sanitizer_out, request)
    
