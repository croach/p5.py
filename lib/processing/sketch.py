from functools import wraps
from multiprocessing import Process
import webbrowser

from .server import SketchProcess, SketchServer


def processing_function(func):
    # Camel case the name to match the Processing naming conventions
    processing_name = ''.join(func.__name__.split('_')[:1] + [s.capitalize() for s in func.__name__.split('_')[1:]])

    # Create a wrapper function that gets the returned args from the real
    # function and creates a new command dict and adds it to the frame queue.
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        cmd = {
            'name': processing_name,
            'args': func(self, *args, **kwargs)
        }
        self.frame.setdefault('commands', []).append(cmd)

    # Mark the method as a Processing function by adding its counterparts name
    wrapper.processing_name = processing_name
    return wrapper


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

    @processing_function
    def point(self, x, y):
        return [x, y]

    @processing_function
    def background(self, color):
        return self._parse_color(color)

    @processing_function
    def fill(self, color):
        return self._parse_color(color)

    @processing_function
    def stroke(self, color):
        return self._parse_color(color)

    @processing_function
    def rect(self, x, y, width, height):
        return [x, y, width, height]

    def _parse_color(self, color):
        try:
            r, g, b = color
        except TypeError:
            r, g, b = [color]*3
        return r, g, b

    @property
    def processing_functions(self):
        for member_name in dir(self):
            obj = getattr(self, member_name)
            if hasattr(obj, 'processing_name'):
                yield obj

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
