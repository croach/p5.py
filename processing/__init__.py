from multiprocessing import Process
import webbrowser
import json
import time

import zmq

from .server import server as _server


class Sketch(object):
    frame_rate = 10

    def setup(self):
        pass

    def draw(self):
        pass

    def run(self):
        producer = Process(target=self._producer, args=(5556,))
        server = Process(target=_server, args=(5556,))
        producer.start()
        server.start()
        webbrowser.open('http://localhost:8888')
        print "Press ctrl-c to exit..."
        try:
            producer.join()
            server.join()
        except KeyboardInterrupt:
            producer.terminate()
            server.terminate()

    def _producer(self, port):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind('tcp://*:%s' % port)
        self.setup()
        while True:
            self.draw()
            # logger.info(dict(data))
            socket.send(json.dumps(self.frame))
            time.sleep(1.0/self.frame_rate)


