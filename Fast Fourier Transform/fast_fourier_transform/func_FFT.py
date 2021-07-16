# reference:  https://www.youtube.com/watch?v=h7apO7q16V0

from cmath import rect, pi
from numpy import linspace
import matplotlib.pyplot as plt

def FFT(P: list):
    """Computes the discrete fourier transform at each value of P (must have length equal to a power of 2)
    equivalent to converting polynomial coefficients to function values
    also equivalent to translating between temporal space and frequency space"""

    # set n to be the value count
    n = len(P)

    # if n is 1, simply return P (base case)
    if n == 1:
        return P

    # compute omega  e**(-2*pi*j / n),  which is 2*pi/n radians along the unit circle in the clockwise
    # direction
    w = rect(1, -2*pi/n)

    # split the polynomial into two parts with half the size of P
    Peven, Podd = P[::2], P[1::2]

    # perform FFT on the smaller polynomials (recursive step)
    Yeven, Yodd = FFT(Peven), FFT(Podd)

    # setup the FFT list of values
    Y = [0]*n

    # loop through each of the n//2 pairs of n complex inputs around the unit circle
    for k in range(n//2):
        # k represents each pair of positive-negative points on the unit circle in the complex plane

        # evaluate the parts of the polynomial with half the degree
        evenPart = Yeven[k]
        oddPart = w**k * Yodd[k]

        # a property of positive-negative pairs allows us to get two function values by simply changing one
        # operation
        Y[k] = evenPart + oddPart
        Y[k + n//2] = evenPart - oddPart

    return Y

# if the inputs of the FFT are y-coordinates then the x-coordinates are simply equally spaced numbers on the
# interval [0, s], where s is an arbitrary scaling factor

# then the output of the FFT are frequency values (in Hertz if x-coordinates are seconds) that are equally spaced
# on the interval [0, (2**n - 1)/s].
