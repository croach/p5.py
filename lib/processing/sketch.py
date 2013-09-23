from functools import wraps
from multiprocessing import Process
import webbrowser

from .utils import processing_func_name


def processing_function(func):
    """Decorator for turning Sketch methods into Processing functions.

    Marks the function it's decorating as a processing function by camel casing
    the name of the function (to follow Processing naming conventions) and
    attaching the new name to the function object as 'processing_name'.

    It also DRY's up the code a bit by creating the command dict from the result
    of calling the wrapped function and appends it to the Sketch object's frame.
    """
    # Camel case the name to match the Processing naming conventions
    processing_name = processing_func_name(func.__name__)

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

    def __init__(self):
        self.reset()
        self.setup()

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
    def background(self, *args):
        return self._parse_color(*args)

    @processing_function
    def fill(self, *args):
        return self._parse_color(*args)

    @processing_function
    def stroke(self, *args):
        return self._parse_color(*args)

    @processing_function
    def no_stroke(self):
        return self._parse_color(0, 0)

    @processing_function
    def stroke_weight(self, weight):
        return [weight]

    @processing_function
    def translate(self, x, y):
        return [x, y]

    @processing_function
    def line(self, x1, y1, x2, y2):
        return [x1, y1, x2, y2]

    @processing_function
    def rect(self, x, y, width, height):
        return [x, y, width, height]

    @processing_function
    def ellipse(self, x, y, width, height):
        return [x, y, width, height]

    def _parse_color(self, *args):
        if len(args) == 1:
            color = [args[0]]*3
        elif len(args) == 2:
            color = [args[0]]*3 + [args[1]]
        else:
            color = args
        return color

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
