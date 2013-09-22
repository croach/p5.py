import os
import json
import signal
import webbrowser

import tornado.web
import tornado.websocket
from tornado import ioloop


# TODO: once this is made into a pip installable package, this will need to be
#       changed and the html files will need to be installed somewhere in the file system.
root = os.path.dirname(__file__)

TEMPLATE_DIR = os.path.join(root, 'templates')


class MainHandler(tornado.web.RequestHandler):
    """Handles new HTTP requests (i.e., it serves the main page (index.html)).
    """
    def get(self):
        self.render('index.html', port=self.application.port)


class WebsocketHandler(tornado.websocket.WebSocketHandler):
    """Handles new websocket connection requests.
    """
    def open(self):
        print 'new connection'
        # self.application.message_handler.register(self.callback)
        # self.application.websockets.append(self)
        self.application.add_connection(self)

    def on_close(self):
        # self.application.message_handler.unregister(self.callback)
        # self.application.websockets.remove(self)
        self.application.remove_connection(self)
        print 'connection closed'

    def on_message(self, message):
        print 'message received', message


class ConnectionHandler(ioloop.PeriodicCallback):
    """Handles all communication for a single websocket connection.

    This class inherits from the Tornado's PeriodicCallback class and is
    scheduled to run periodically (according to the given sketch's frame rate)
    on the main IO Loop instance. At each time step, the step method is called
    which is responsible for advancing the current frame of the sketch object
    and sending the frame information to the client.

    TODO: add some comments on receiving communication from the client.

    """
    def __init__(self, connection, sketch):
        self.connection = connection
        self.sketch = sketch
        super(ConnectionHandler, self).__init__(self.step, 1000.0/self.sketch.frame_rate)

    def step(self):
        self.sketch.draw()
        self.connection.write_message(json.dumps(self.sketch.frame))
        self.sketch.reset()


class SketchApplication(tornado.web.Application):
    """Wraps a Sketch and handles all communication with the client(s).

    This Tornado app ties together the MainHandler instance (responsible for
    handling all new browser connections), and the WebSocketHandler instance
    (responsible for handling all new websocket connections).

    It takes a Sketch class and an optional port number, the latter of which it
    listens on for new HTTP connection requests. When a new connection is
    initiated, it creates an instance of the given Sketch class and starts a
    ConnectionHandler that is responsible for stepping the sketch object through
    each frame and returning the inforamtion to the client.

    """

    def __init__(self, sketch_class, port=8000):
        self.sketch_class = sketch_class
        self.port = port
        self.connection_handlers = {}
        handlers = [
            (r'/ws', WebsocketHandler),
            (r'/', MainHandler)
        ]
        settings = {
            "template_path": os.path.join(TEMPLATE_DIR)
        }
        super(SketchApplication, self).__init__(handlers, **settings)


    def run(self):
        """Runs the sketch application.

        This method starts up the Tornado HTTP and websocket servers. It also
        open the user's browser to sketch's URL and sets up a signal handler to
        capture Ctrl-C events to shutdown the applcation. Finally it starts the
        IO Loop.

        """
        # Start listening for new browser connections
        self.listen(self.port)

        url = 'http://localhost:%d' % self.port
        webbrowser.open(url)
        print 'Visualialization available on %s' % url
        print "Press ctrl-c to exit..."

        # TODO: Look into using IOLoop.add_callback_from_signal to capture
        #       the Ctrl-c (signal.SIGINT) signal and exit gracefully.
        def sig_handler(sig, frame):
            ioloop.IOLoop.instance().add_callback_from_signal(self.shutdown)
        signal.signal(signal.SIGINT, sig_handler)

        ioloop.IOLoop.instance().start()

    def add_connection(self, connection):
        handler = ConnectionHandler(connection, self.sketch_class())
        handler.start()
        self.connection_handlers[hash(connection)] = handler

    def remove_connection(self, connection):
        handler = self.connection_handlers.pop(hash(connection))
        handler.stop()

    def shutdown(self):
        """Shuts down the application.

        Stops all active connection handlers and the Tornado IO Loop.

        """
        print "\nStopping all active connections..."
        while True:
            try:
                _, connection_handler = self.connection_handlers.popitem()
                connection_handler.stop()
            except KeyError:
                break

        print "Shutting down the Server..."
        ioloop.IOLoop.instance().stop()


