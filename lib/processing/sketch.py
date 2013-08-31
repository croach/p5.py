from multiprocessing import Process
import webbrowser

from .server import SketchProcess, SketchServer


def foo(func):

    def wrapper(*args, **kwargs):
        cmd = {'name': 'background', 'args': [r, g, b]}
        self.frame.setdefault('commands', []).append(cmd)

class Sketch(object):
    frame_rate = 60
    width = 100
    height = 100

    def setup(self):
        pass

    def draw(self):
        pass

    def run(self, port=8000):
        worker = Process(target=SketchProcess(self))
        server = Process(target=SketchServer(port))
        worker.start()
        server.start()
        url = 'http://localhost:%d' % port
        webbrowser.open(url)
        print 'Visualialization available on %s' % url
        print "Press ctrl-c to exit..."
        try:
            worker.join()
            server.join()
        except KeyboardInterrupt:
            worker.terminate()
            server.terminate()

    def __init__(self):
        self.reset()

    def reset(self):
        """Resets the state of the system (i.e., the current frame dict).

        This method is meant to be called between calls to the draw method
        as a means of clearing the current frame. The frame is the set of
        commands to be sent to the client for drawing the current frame.
        """
        self._frame = {}

    def point(self, x, y):
        cmd = {'name': 'point', 'args': [x, y]}
        self.frame.setdefault('commands', []).append(cmd)

    def background(self, color):
        r, g, b = self._parse_color(color)
        cmd = {'name': 'background', 'args': [r, g, b]}
        self.frame.setdefault('commands', []).append(cmd)

    def fill(self, color):
        r, g, b = self._parse_color(color)
        cmd = {'name': 'fill', 'args': [r, g, b]}
        self.frame.setdefault('commands', []).append(cmd)

    def stroke(self, color):
        r, g, b = self._parse_color(color)
        cmd = {'name': 'stroke', 'args': [r, g, b]}
        self.frame.setdefault('commands', []).append(cmd)

    def rect(self, x, y, width, height):
        cmd = {'name': 'rect', 'args': [x, y, width, height]}
        self.frame.setdefault('commands', []).append(cmd)

    def _parse_color(self, color):
        try:
            r, g, b = color
        except TypeError:
            r, g, b = [color]*3
        return r, g, b


    @property
    def frame(self):
        self._frame.update({
            'canvas': {
                'width': self.width,
                'height': self.height
            }
        })
        return self._frame

    @frame.setter
    def frame(self, frame):
        self._frame = frame
