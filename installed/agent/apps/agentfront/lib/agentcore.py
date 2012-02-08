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

"""Library to communicate back and forth between webserver and back end engines
"""

__authors__ = [
    '"Kailash Budhathoki" <kailash.buki@gmail.com>'
]


import json
import logging
import uuid

import gevent
from gevent_zeromq import zmq

import agentcore


class AgentWsInWire: 
    def __init__(self):
        self.create_agent_webserver_in()
    
    def create_agent_webserver_in(self):
        zmq_context = zmq.Context()
        self.socket = zmq_context.socket(zmq.XREP)
        self.socket.bind('tcp://127.0.0.1:9001')
       
    def recv_request(self):
        return self.socket.recv_multipart()
        
    def reply(self, identity, response):
        return self.socket.send_multipart((identity, response))
        
class AgentAnalyticsInWire: 
    def __init__(self):
        self.create_agent_analytics_in()
    
    def create_agent_analytics_in(self):
        zmq_context = zmq.Context()
        self.socket = zmq_context.socket(zmq.PULL)
        self.socket.connect('tcp://127.0.0.1:9006')
       
    def recv_request(self):
        return self.socket.recv_json()

class AgentPushWire:
    def __init__(self):
        self.create_agent_other_wire()
        
    def create_agent_other_wire(self):
        zmq_context = zmq.Context()
        self.socket = zmq_context.socket(zmq.PUSH)
        self.socket.bind('tcp://127.0.0.1:9002')
        
    def send(self, req):
        return self.socket.send_json(req)

def analyzer_listener(ag_a_in, ag_ws_in, identity_cache):
    """
    """
    print 'id cache=%s' % identity_cache
    while True:
        response = ag_a_in.recv_request()
        logging.warn('AGENTCORE: Received request from analyzer.')
        if response.has_key('from_analytics'):
            identity = response.get('identity')
            match = response.get('match')
            if 'match' in response and 'identity' in response:
                act_identity = identity_cache.pop(identity, None)
                #TODO (kailash.buki@gmail.com): Raise exception in case identity is
                #                               not found in cache
                response = json.dumps(dict(match=match))
                logging.warn('AGENTCORE: Replying back to the webserver. %s' % response)
                ag_ws_in.reply(act_identity, response)
            else:
                logging.warn('AGENTCORE: Invalid parameters in the request from analyzer.')
    
def _dispatch_request(ag_ws_in, ag_push, ag_a_in, identity, identity_cache, request):
    """dispatches the request to different engines based on the type of request

    Args: 
        ag_ws_in: zmq socket for communication with webserver
        ag_push: zmq socket for communication with preprocessor
        ag_a_in: zmq socket for receiving results from analyzer
        identity_cache: mapping of original identity to the unique id
        request: request parameters

    Returns: None
    """
    pdf_path = request.get('pdf_path')
    do_what = request.get('do_what')

    if 'pdf_path' in request and 'do_what' in request:
        uid = uuid.uuid4().hex
        identity_cache[uid] = identity
        req = dict(pdf_path=pdf_path, do_what=do_what, identity=uid)
        logging.warn('AGENTCORE: Pushing the request to the preprocessor. %s' % req)
        ag_push.send(req)
    else:
        logging.warn('AGENTCORE: Invalid parameters in the request from webserver.')

def start():
    """starts the agent core
    """
    identity_cache = {}
    ag_ws_in = AgentWsInWire()
    ag_push = AgentPushWire()
    ag_a_in = AgentAnalyticsInWire()

    while True:
        logging.warn('AGENTCORE: Agent listening to incoming requests')
        identity, request = ag_ws_in.socket.recv_multipart()
        request = eval(request)
        
        gevent.spawn_link_exception(_dispatch_request, ag_ws_in, ag_push, ag_a_in, identity, identity_cache, request)
        gevent.spawn_link_exception(analyzer_listener, ag_a_in, ag_ws_in, identity_cache)
