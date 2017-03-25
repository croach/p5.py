import os
import inspect
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
    def __init__(self, *args, **kwargs):
        super(WebsocketHandler, self).__init__(*args, **kwargs)
        self.message_handlers = []

    def open(self):
        print('new connection')
        self.application.add_connection(self)

    def on_close(self):
        self.application.remove_connection(self)
        print('connection closed')

    def on_message(self, message):
        for handler in self.message_handlers:
            handler(message)

    def add_message_handler(self, callback):
        self.message_handlers.append(callback)

    def remove_message_handler(self, callback):
        self.message_handlers.remove(callback)


class ConnectionHandler(ioloop.PeriodicCallback):
    """Handles all communication between a sketch and its client(s).

    This class inherits from the Tornado's PeriodicCallback class and is
    scheduled to run periodically (according to the given sketch's frame rate)
    on the main IO Loop instance. At each time step, the step method is called
    which is responsible for advancing the current frame of the sketch object
    and sending the frame information to the client(s).

    TODO: add some comments on receiving communication from the client.

    """
    def __init__(self, sketch, connection=None):
        self.sketch = sketch
        self.sketch.setup()
        # TODO: Once issue #11 is resolved, there will no longer be a need for
        # multiple connections. A ConnectionHandler instance will instead be
        # created for every new connection. So, the connections attribute below
        # can be changed to a single connection attribute and the add_connection
        # and remove_connection methods can be removed. Also, the loop in step
        # can be removed and replace with a single write.
        self.connections = []
        if connection is not None:
            connection.add_message_handler(self.handle_message)
            self.connections.append(connection)
        super(ConnectionHandler, self).__init__(self.step, 1000.0/self.sketch.frame_rate)

    def step(self):
        self.sketch.draw()
        message = json.dumps(self.sketch.frame)
        for connection in self.connections:
            connection.write_message(message)
        self.sketch.reset()

    def add_connection(self, connection):
        connection.add_message_handler(self.handle_message)
        self.connections.append(connection)

    def remove_connection(self, connection):
        self.connections.remove(connection)

    def handle_message(self, message):
        data = json.loads(message)
        for key, value in data.items():
            setattr(self.sketch, key, value)


class SketchApplication(tornado.web.Application):
    """Wraps a Sketch and handles all communication with the client(s).

    This Tornado app ties together the MainHandler instance (responsible for
    handling all new browser connections), and the WebSocketHandler instance
    (responsible for handling all new websocket connections).

    It takes a Sketch class and an optional port number, the latter of which
    it listens on for new HTTP connection requests. When a new connection is
    initiated, it creates an instance of the given Sketch class and starts a
    ConnectionHandler that is responsible for stepping the sketch object
    through each frame and returning the inforamtion to the client.

    """

    def __init__(self, sketch_class_or_instance, port=8000):
        self.port = port
        self.sketch_class_or_instance = sketch_class_or_instance
        self.connection_handlers = {}
        if not inspect.isclass(self.sketch_class_or_instance):
            handler = ConnectionHandler(self.sketch_class_or_instance)
            handler.start()
            self.connection_handlers[hash(handler)] = handler


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
        open the user's browser to sketch's URL and sets up a signal handler
        to capture Ctrl-C events to shutdown the applcation. Finally it starts
        the IO Loop.

        """
        # Start listening for new browser connections
        self.listen(self.port)

        url = 'http://localhost:%d' % self.port
        webbrowser.open(url)
        print('Visualialization available on %s' % url)
        print("Press ctrl-c to exit...")

        # TODO: Look into using IOLoop.add_callback_from_signal to capture
        #       the Ctrl-c (signal.SIGINT) signal and exit gracefully.
        def sig_handler(sig, frame):
            ioloop.IOLoop.instance().add_callback_from_signal(self.shutdown)
        signal.signal(signal.SIGINT, sig_handler)

        ioloop.IOLoop.instance().start()

    def add_connection(self, connection):
        if inspect.isclass(self.sketch_class_or_instance):
            handler = ConnectionHandler(self.sketch_class_or_instance(), connection)
            handler.start()
            self.connection_handlers[hash(connection)] = handler
        else:
            list(self.connection_handlers.values())[0].add_connection(connection)

    def remove_connection(self, connection):
        if inspect.isclass(self.sketch_class_or_instance):
            handler = self.connection_handlers.pop(hash(connection))
            handler.stop()
        else:
            list(self.connection_handlers.values())[0].remove_connection(connection)

    def shutdown(self):
        """Shuts down the application.

        Stops all active connection handlers and the Tornado IO Loop.

        """
        print("\nStopping all active connections...")
        while True:
            try:
                _, connection_handler = self.connection_handlers.popitem()
                connection_handler.stop()
            except KeyError:
                break

        print("Shutting down the Server...")
        ioloop.IOLoop.instance().stop()
