import __builtin__

import argparse
import types
from functools import wraps

from . import mathfuncs
from .pvector import PVector
from .sketch import Sketch
from .server import SketchApplication
from .utils import processing_func_name


# TODO: Add an __all__ variable to make sure everything doesn't get imported
#       when the user does an import *


class SingletonSketch(Sketch):

    _mouseX = 0
    _mouseY = 0
    _mousePressed = False

    def get_mouseX(self):
        return self._mouseX
    def set_mouseX(self, mouseX):
        self._mouseX = mouseX
        __builtin__.mouseX = mouseX
    mouseX = property(get_mouseX, set_mouseX)

    def get_mouseY(self):
        return self._mouseY
    def set_mouseY(self, mouseY):
        self._mouseY = mouseY
        __builtin__.mouseY = mouseY
    mouseY = property(get_mouseY, set_mouseY)

    def get_mousePressed(self):
        return self._mousePressed
    def set_mousePressed(self, mousePressed):
        self._mousePressed = mousePressed
        __builtin__.mousePressed = mousePressed
    mousePressed = property(get_mousePressed, set_mousePressed)


_sketch = SingletonSketch()

# Adding global variables to the __builtin__ module
__builtin__.width = _sketch.width
__builtin__.height = _sketch.height
# TODO: is there a way to have a frameRate function and variable on __builtin__?
__builtin__.frame_rate = _sketch.frame_rate
__builtin__.mouseX = _sketch.mouseX
__builtin__.mouseY = _sketch.mouseY
__builtin__.mousePressed = _sketch.mousePressed


def size(width, height):
    __builtin__.width = _sketch.width = width
    __builtin__.height = _sketch.height = height


def frameRate(frame_rate):
    __builtin__.frameRate = _sketch.frame_rate = frame_rate


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

    # Define and parse the command line arguments
    parser = argparse.ArgumentParser(description='Runs a p5.py script.')
    parser.add_argument('--port', '-p', type=int, default=8000,
                        help='port the p5 server is listening on')
    args = parser.parse_args()

    # TODO: Replace this with something a bit more dynamic
    if 'setup' in main_globals:
        _bind(__main__.setup, _sketch)
    if 'draw' in main_globals:
        _bind(__main__.draw, _sketch)

    SketchApplication(_sketch, port=args.port).run()


# Add the processing functions to the current module
self = __import__(__name__)
for func in _sketch.processing_functions:
    setattr(self, func.processing_name, func)

for func_name in filter(lambda s: not s.startswith('_'), dir(mathfuncs)):
    func = getattr(mathfuncs, func_name)
    processing_name = processing_func_name(func_name)

    # if the new function's name matches a builtin one, add a preceding
    # underscore to the builtin functions name so we don't overwrite it.
    if processing_name in dir(__builtin__):
        builtin_func = getattr(__builtin__, processing_name)
        setattr(__builtin__, '_%s' % processing_name, builtin_func)

    setattr(self, processing_name, func)
