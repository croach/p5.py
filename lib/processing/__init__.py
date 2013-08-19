import types
from functools import wraps

from .sketch import Sketch


# TODO: Add an __all__ variable to make sure everything doesn't get imported
#       when the user does an import *

# Adding global variables to the __builtin__ module
import __builtin__
__builtin__.width = 100
__builtin__.height = 100

_sketch = Sketch()

# TODO: Replace these methods with something a bit more dynamic
def point(x, y):
    _sketch.point(x, y)

def background(color):
    _sketch.background(color)

def fill(color):
    _sketch.fill(color)

def stroke(color):
    _sketch.stroke(color)

def rect(x, y, w, h):
    _sketch.rect(x, y, w, h)

def size(width, height):
    __builtin__.width = _sketch.width = width
    __builtin__.height = _sketch.height = height

def _bind(fn, obj):
    """Turns a function into a bound method and adds it to the given object.
    """
    @wraps(fn)
    def method(self, *args, **kwargs):
        return fn(*args, **kwargs)

    bound_method = types.MethodType(method, obj, obj.__class__)
    setattr(obj, bound_method.__name__, bound_method)

def run():
    import __main__
    main_globals = dir(__main__)

    # TODO: Replace this with something a bit more dynamic
    if 'setup' in main_globals:
        _bind(__main__.setup, _sketch)
    if 'draw' in main_globals:
        _bind(__main__.draw, _sketch)

    _sketch.run()
