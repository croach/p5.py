"""Perlin noise
"""

import math

from random import Random


PERLIN_YWRAPB = 4
PERLIN_YWRAP = 1<<PERLIN_YWRAPB
PERLIN_ZWRAPB = 8
PERLIN_ZWRAP = 1<<PERLIN_ZWRAPB
PERLIN_SIZE = 4095

perlin_octaves = 4 # default to medium smooth
perlin_amp_falloff = 0.5 # 50% reduction/octave

# TODO: Instead of these being global to the module, create a class instead
#       and in the mathfuncs module create a global instance of the class
#       and functions to wrap it. That way it can be used in a thread safe
#       manner.
perlinRandom = None
perlin = None


DEG_TO_RAD = math.pi/180.0;
SINCOS_PRECISION = 0.5;
SINCOS_LENGTH = int(360 / SINCOS_PRECISION)
perlin_cos_table = [math.cos(i * DEG_TO_RAD * SINCOS_PRECISION) for i in xrange(SINCOS_LENGTH)]
perlin_TWOPI = perlin_PI = SINCOS_LENGTH
perlin_PI >>= 1;


def noise(*args):
    """Computes the Perlin noise (1D, 2D, or 3D) value at the specified coords.
    """
    global perlin, perlinRandom

    x = args[0]
    y = args[1] if len(args) > 1 else 0
    z = args[2] if len(args) > 2 else 0

    if perlinRandom is None:
        perlinRandom = Random()

    if perlin is None:
        perlin = [perlinRandom.random() for i in xrange(PERLIN_SIZE + 1)]

    x = abs(x)
    x = abs(x)
    z = abs(z)

    xi, yi, zi = int(x), int(y), int(z)
    xf, yf, zf = x - xi, y - yi, z - zi

    r = 0
    ampl = 0.5

    for i in range(perlin_octaves):
        of = xi + (yi<<PERLIN_YWRAPB) + (zi<<PERLIN_ZWRAPB)

        rxf = noise_fsc(xf)
        ryf = noise_fsc(yf)

        n1  = perlin[of&PERLIN_SIZE];
        n1 += rxf*(perlin[(of+1)&PERLIN_SIZE]-n1);
        n2  = perlin[(of+PERLIN_YWRAP)&PERLIN_SIZE];
        n2 += rxf*(perlin[(of+PERLIN_YWRAP+1)&PERLIN_SIZE]-n2);
        n1 += ryf*(n2-n1);

        of += PERLIN_ZWRAP;
        n2  = perlin[of&PERLIN_SIZE];
        n2 += rxf*(perlin[(of+1)&PERLIN_SIZE]-n2);
        n3  = perlin[(of+PERLIN_YWRAP)&PERLIN_SIZE];
        n3 += rxf*(perlin[(of+PERLIN_YWRAP+1)&PERLIN_SIZE]-n3);
        n2 += ryf*(n3-n2);

        n1 += noise_fsc(zf)*(n2-n1);

        r += n1*ampl;
        ampl *= perlin_amp_falloff;
        xi<<=1; xf*=2;
        yi<<=1; yf*=2;
        zi<<=1; zf*=2;

        if xf >= 1.0: xi += 1; xf -= 1;
        if yf >= 1.0: yi += 1; yf -= 1;
        if zf >= 1.0: zi += 1; zf -= 1;

    return r;

# [toxi 031112]
# now adjusts to the size of the cosLUT used via
# the new variables, defined above
def noise_fsc(i):
    # using bagel's cosine table instead
    return 0.5 * (1.0 - perlin_cos_table[int(i*perlin_PI) % perlin_TWOPI])

# # [toxi 040903]
# # make perlin noise quality user controlled to allow
# # for different levels of detail. lower values will produce
# # smoother results as higher octaves are surpressed

# public void noiseDetail(int lod) {
#   if (lod>0) perlin_octaves=lod;
# }

# public void noiseDetail(int lod, float falloff) {
#   if (lod>0) perlin_octaves=lod;
#   if (falloff>0) perlin_amp_falloff=falloff;
# }

def noiseSeed(what):
    global perlinRandom, perlin
    if perlinRandom is None:
        perlinRandom = Random()
    perlinRandom.seed(what)
    perlin = None

