import os
import sys
import json
import webbrowser
import logging

import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

ioloop.install()

import tornado.web
import tornado.websocket
import tornado.ioloop

# TODO: once all connections have closed, send a message back to the main
#       process letting it know it is ok for it to kill the subprocesses.

# port = sys.argv[1]
# level = sys.argv[2].upper() if len(sys.argv) > 2 else 'WARN'
# level = logging.INFO
# logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(getattr(logging, level))

root = os.path.dirname(__file__)

def server(port):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://localhost:%s' % port)
    socket.setsockopt(zmq.SUBSCRIBE, '')

    class Consumer(object):
        def __init__(self):
            self.connections = []

        def __call__(self, message):
            # logger.info('Message received: %s' % message)
            for connection in self.connections:
                connection.write_message(message[0])

    consumer = Consumer()
    stream = ZMQStream(socket)
    stream.on_recv(consumer)

    class WSHandler(tornado.websocket.WebSocketHandler):
        def open(self):
            print 'new connection'
            consumer.connections.append(self)

        def on_close(self):
            consumer.connections.remove(self)
            print 'connection closed'

        def on_message(self, message):
            print 'message received', message

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.render('index.html')

    application = tornado.web.Application([
        (r'/ws', WSHandler),
        (r'/', MainHandler)
    ])


    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
