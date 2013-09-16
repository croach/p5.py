import random as _random

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
