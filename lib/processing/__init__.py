import types
import random as _random
from functools import wraps

from .sketch import Sketch


# TODO: Add an __all__ variable to make sure everything doesn't get imported
#       when the user does an import *

# Adding global variables to the __builtin__ module
import __builtin__
__builtin__.width = 100
__builtin__.height = 100

_sketch = Sketch()

# Add the processing functions to the current module
self = __import__(__name__)
for func in _sketch.processing_functions:
    setattr(self, func.processing_name, func)

# Random

def random(*args):
    """Generates random numbers.

    Each time the random() function is called, it returns an unexpected value
    within the specified range. If only one parameter is passed to the function,
    it will return a float between zero and the value of the high parameter.
    For example, random(5) returns values between 0 and 5 (starting at zero,
    and up to, but not including, 5).

    If two parameters are specified, the function will return a float with a
    value between the two values. For example, random(-5, 10.2) returns values
    starting at -5 and up to (but not including) 10.2. To convert a
    floating-point random number to an integer, use the int() function.

    Arguments:
    low -- lower limit
    high -- upper limit

    Returns:
    float
    """
    low = args[0] if len(args) > 1 else 0
    high = args[1] if len(args) > 1 else args[0]
    offset = _random.random() * (high - low)
    return low + offset

def random_seed(seed):
    """Sets the seed value for random().

    By default, random() produces different results each time the program is
    run. Set the seed parameter to a constant to return the same pseudo-random
    numbers each time the software is run.

    Arguments:
    seed -- seed value
    """
    _random.seed(seed)


def size(width, height):
    __builtin__.width = _sketch.width = width
    __builtin__.height = _sketch.height = height

# TODO: Make sure this matches the one in Processing
def constrain(amt, low, high):
    """Constrains a value to not exceed a maximum and minimum value.
    """
    if amt < low:
        return low
    elif amt > high:
        return high
    else:
        return amt


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
