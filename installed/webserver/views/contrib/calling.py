from gevent_zeromq import zmq

def agent_req_dispatcher():
    zmq_context = zmq.Context()
    socket = zmq_context.socket(zmq.XREQ)
    socket.connect('tcp://127.0.0.1:9001')
    return socket