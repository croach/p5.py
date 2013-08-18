import os
import json
import sys
import time
import webbrowser
import logging

import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

ioloop.install()

import tornado.web
import tornado.websocket
import tornado.ioloop


# TODO: once this is made into a pip installable package, this will need to be
#       changed and the html files will need to be installed somewhere in the file system.
root = os.path.dirname(__file__)

TEMPLATE_DIR = os.path.join(root, 'templates')

ZMQ_PORT = 5556


class SketchProcess(object):
    """Worker process that runs a sketch.

    This is a stand alone worker (system) process that wraps a Sketch instance
    and is essentially a discrete event loop. It loops until the sketch instance
    tells it to stop, or it is interrupted by the main process and calls the
    draw method on the sketch to produce the visualization data for the current
    time step. It then sends the data for the current time step to the message
    handler to be dispatched to all of the attached clients.
    """
    def __init__(self, sketch):
        self.sketch = sketch

    def __call__(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind('tcp://*:%s' % ZMQ_PORT)
        self.sketch.setup()
        while True:
            self.sketch.draw()
            # logger.info(dict(data))
            socket.send(json.dumps(self.sketch.frame))
            time.sleep(1.0/self.sketch.frame_rate)


class SketchMessageHandler(object):
    """Intermediary message handler for a discrete event simulation.

    SketchMessageHandler acts a bit like a chat server. It has a simple API
    through which callback functions can be registered. It then listens for
    new messages from the sketch process(es) and relays the new data to each
    of the clients through the registered callback functions.
    """
    def __init__(self):
        self.callbacks = []

        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect('tcp://localhost:%s' % ZMQ_PORT)
        socket.setsockopt(zmq.SUBSCRIBE, '')
        stream = ZMQStream(socket)
        stream.on_recv(self.message_received)

    def message_received(self, message):
        for callback in self.callbacks:
            callback(message[0])

    def register(self, callback):
        self.callbacks.append(callback)

    def unregister(self, callback):
        self.callbacks.remove(callback)


class MainHandler(tornado.web.RequestHandler):
    """Serves the main page (index.html).
    """
    def get(self):
        self.render('index.html', port=self.application.port)


class WebsocketHandler(tornado.websocket.WebSocketHandler):
    """Handles websocket connections.
    """
    def open(self):
        print 'new connection'
        self.application.message_handler.register(self.callback)

    def on_close(self):
        self.application.message_handler.unregister(self.callback)
        print 'connection closed'

    def on_message(self, message):
        print 'message received', message

    def callback(self, message):
        """Callback function registered with the sketch message handler.
        """
        self.write_message(message)


class SketchApplication(tornado.web.Application):
    """Tornado app that handles all communication with the client(s) (browser).

    The main reason for a custom application is to give each of the websocket
    handler instances access to the SketchMessageHandler instance so they can
    register their callback methods with it.
    """
    def __init__(self, port):
        self.port = port
        self.message_handler = SketchMessageHandler()
        handlers = [
            (r'/ws', WebsocketHandler),
            (r'/', MainHandler),
            # (r'/static/(.*)', tornado.web.StaticFileHandler, {"path": JS_DIR}),
        ]
        settings = {
            "template_path": os.path.join(TEMPLATE_DIR)
            # "debug": True,
        }
        super(SketchApplication, self).__init__(handlers, **settings)


class SketchServer(object):
    """A tornado based web and websocket server for the sketch.

    The SketchServer is a tornado based web server that handles all
    communication with the client (the browser). It essentially wraps into
    one bundle instances of the websocket, index, and sketch message handlers.
    """
    def __init__(self, port):
        self.port = port

    def __call__(self):
        application = SketchApplication(self.port)
        application.listen(self.port)
        tornado.ioloop.IOLoop.instance().start()
