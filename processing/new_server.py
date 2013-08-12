import os


root = os.path.dirname(__file__)


class Producer(object):
    """Produces data for rendering by running the sketch.
    """
    def __init__(self, sketch):
        self.sketch = sketch

class Consumer(object):
    """Consumes data from the producer calling registered callbacks upon receipt
    """
    def __init__(self):
        pass

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class WebsocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(consumer, *args, **kwargs):
        self.consumer

    def open(self):
        print 'new connection'
        self.consumer.register_callback(self.callback)

    def on_close(self):
        self.connections.remove(self)
        print 'connection closed'

    def on_message(self, message):
        print 'message received', message

    def on_update(self, message):
        """Producer update handler

        This method is called everytime a new update is received from the
        producer.
        """
        for connection in self.connections:
            connection.write_message(message[0])

