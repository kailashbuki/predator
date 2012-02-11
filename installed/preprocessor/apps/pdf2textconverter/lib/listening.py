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
import logging

from gevent_zeromq import zmq

from converting import convert_pdf2textfile


def _create_pdf2textconverter_in(zmq_context):
    """zmq socket is created for incoming requests
    
    Args:
        zmq_context: zmq context
    
    Returns: 
        A zmq socket for listening incoming requests
    """
    zmq_socket = zmq_context.socket(zmq.PULL)
    zmq_socket.connect('tcp://127.0.0.1:9002')
    
    return zmq_socket

def _create_pdf2textconverter_out(zmq_context):
    """zmq socket is created for publishing messages
    
    Args:
        zmq_context: zmq context
    
    Returns: 
        A zmq socket for dispatching results
    """
    zmq_socket = zmq_context.socket(zmq.PUSH)
    zmq_socket.bind('tcp://127.0.0.1:9003')
    
    return zmq_socket    

def _process_request(pdf2textconverter_out, request):
    """processes the request coming to the pdf2textconverter engine
    in a separate greenlet

    Args: 
        pdf2textconverter_out: outgoing zmq socket
        request: request parameter from agent
    
    Returns: None
    """
    do_what = request.get('do_what')
    identity = request.get('identity')
    pdf_path = request.get('pdf_path')

    if 'pdf_path' in request and 'do_what' in request and 'identity' in request:
        
        logging.debug('PREPROCESSOR: Converting to the text format ...')
        textfilepath = convert_pdf2textfile(pdf_path)

        if textfilepath:
            logging.debug('PREPROCESSOR: Pushing the result to the santizer ...')
            pdf2textconverter_out.send_json(dict(
                                            do_what = do_what, 
                                            identity = identity, 
                                            text_path = textfilepath))

        else:
            logging.warn('PREPROCESSOR: Error encountered while converting pdf file to text file.')
    
    else:
        logging.warn('PREPROCESSOR: Unknown parameters in the request to the preprocessor.')



def listener_loop_runner():
    """Runs the loop to listen to the incoming requests and dispatch the task to
    another engine
    
    Args:
        None
    
    Returns: None
    """
    zmq_context = zmq.Context()
    pdf2textconverter_in = _create_pdf2textconverter_in(zmq_context)
    pdf2textconverter_out = _create_pdf2textconverter_out(zmq_context)
    
    while True:
        request = pdf2textconverter_in.recv_json()
        logging.debug('PREPROCESSOR: Received request %s' % request)
        gevent.spawn_link_exception(_process_request, pdf2textconverter_out, request)
