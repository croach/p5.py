import random as _random

from .perlin import noise, noiseSeed

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

def random_gaussian():
    """Returns a float from a random series of numbers.

    Each time the randomGaussian() function is called, it returns a number
    fitting a Gaussian, or normal, distribution having a mean of 0 and a
    standard deviation of 1. There is theoretically no minimum or maximum value
    that randomGaussian() might return. Rather, there is just a very low
    probability that values far from the mean will be returned; and a higher
    probability that numbers near the mean will be returned.

    """
    return _random.gauss(0, 1)

def random_seed(seed):
    """Sets the seed value for random().

    By default, random() produces different results each time the program is
    run. Set the seed parameter to a constant to return the same pseudo-random
    numbers each time the software is run.

    Arguments:
    seed -- seed value

    """
    _random.seed(seed)


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

def map(value, start1, stop1, start2, stop2):
    """Re-maps a number from one range to another.
    """
    return (value - start1) / float(stop1 - start1) * (stop2 - start2) + start2


# def noise(*args):
#     """Returns the Perlin noise value at specified coordinates.

#     Perlin noise is a random sequence generator producing a more natural,
#     harmonic succession of numbers than that of the standard random() function.
#     It was invented by Ken Perlin in the 1980s and has been used in graphical
#     applications to generate procedural textures, shapes, terrains, and other
#     seemingly organic forms.

#     In contrast to the random() function, Perlin noise is defined in an infinite
#     n-dimensional space, in which each pair of coordinates corresponds to a
#     fixed semi-random value (fixed only for the lifespan of the program). The
#     resulting value will always be between 0.0 and 1.0. Processing can compute
#     1D, 2D and 3D noise, depending on the number of coordinates given. The noise
#     value can be animated by moving through the noise space, as demonstrated in
#     the first example above. The 2nd and 3rd dimensions can also be interpreted
#     as time.

#     The actual noise structure is similar to that of an audio signal, in respect
#     to the function's use of frequencies. Similar to the concept of harmonics in
#     physics, Perlin noise is computed over several octaves which are added
#     together for the final result.

#     Another way to adjust the character of the resulting sequence is the scale
#     of the input coordinates. As the function works within an infinite space,
#     the value of the coordinates doesn't matter as such; only the distance
#     between successive coordinates is important (such as when using noise()
#     within a loop). As a general rule, the smaller the difference between
#     coordinates, the smoother the resulting noise sequence. Steps of 0.005-0.03
#     work best for most applications, but this will differ depending on use.

#     """
#     if len(args) == 1:
#         return pnoise1(*args)
#     if len(args) == 2:
#         return pnoise2(*args)
#     if len(args) == 3:
#         return pnoise3(*args)

