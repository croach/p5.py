from multiprocessing import Process
import webbrowser
import time

import zmq

from .server import SketchProcess, SketchServer

try:
    import simplejson as json
except ImportError:
    import json


class Sketch(object):
    frame_rate = 10

    def setup(self):
        pass

    def draw(self):
        pass

    def run(self, port=8000):
        worker = Process(target=SketchProcess(self))
        server = Process(target=SketchServer(port))
        worker.start()
        server.start()
        webbrowser.open('http://localhost:%d' % port)
        print "Press ctrl-c to exit..."
        try:
            worker.join()
            server.join()
        except KeyboardInterrupt:
            worker.terminate()
            server.terminate()
