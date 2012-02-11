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

from comparing import compare


def _create_analyzer_out(zmq_context):
    """zmq socket is created for publishing messages
    
    Args:
        zmq_context: zmq context
    
    Returns: 
        A zmq socket for dispatching results
    """
    zmq_socket = zmq_context.socket(zmq.PUSH)
    zmq_socket.bind('tcp://127.0.0.1:9006')

    return zmq_socket

def _create_analyzer_in(zmq_context):
    """zmq socket is created for incoming requests. Incoming requests come from
    pdf2textconverter app
    
    Args:
        zmq_context: zmq context
    
    Returns: 
        A zmq socket for listening incoming requests
    """
    zmq_socket = zmq_context.socket(zmq.PULL)
    zmq_socket.connect('tcp://127.0.0.1:9005')
    
    return zmq_socket

def _process_request(analyzer_out, request):
    """processes the incoming requests to comparator engine in a separate greenlet

    Args: 
        analyzer_out: dispatching zmq socket
        request: request paramter

    Returns: None
    """
    if 'fingerprints' in request and 'identity' in request:
        logging.debug('Comparing fingerprints ...')
        match = compare(request.get('fingerprints'))
        logging.debug('ANALYZER: Document fingerints match complete with the db.')
        response = dict(
                    match = match, 
                    identity = request.get('identity'), 
                    from_analytics=True)
        logging.debug('ANALYZER: Sending the match to agentcore. %s' % match)
        analyzer_out.send_json(response)
    else:
        logging.warn('ANALYZER: Unknown parameters in the request to analyzer.')


def listener_loop_runner():
    """Runs the loop to listen to the incoming requests and dispatch the task to
    another engine
    
    Args:
        None
    
    Returns: None
    """
    zmq_context = zmq.Context()
    analyzer_in = _create_analyzer_in(zmq_context)
    analyzer_out = _create_analyzer_out(zmq_context)

    while True:
        request = analyzer_in.recv_json()
        logging.debug('ANALYZER: Received request ...')
        
        gevent.spawn_link_exception(_process_request, analyzer_out, request)
