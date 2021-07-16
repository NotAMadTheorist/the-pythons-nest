# reference:  https://www.youtube.com/watch?v=h7apO7q16V0
from cmath import rect, pi

def IFFT_re(P: list):
    """Computes the discrete inverse fourier transform at each value of P (must have length equal to a power of 2)
    equivalent to converting function values to polynomial coefficients fitting them
    also equivalent to translating between frequency space and temporal space"""

    # set n to be the value count
    n = len(P)

    # if n is 1, simply return P (base case)
    if n == 1:
        return P

    # compute omega  e**(-2*pi*j / n),  which is 2*pi/n radians along the unit circle in the counter-clockwise
    # direction
    w = rect(1, 2*pi/n)

    # split the polynomial into two parts with half the size of P
    Peven, Podd = P[::2], P[1::2]

    # perform IFFT on the smaller polynomials (recursive step)
    Yeven, Yodd = IFFT_re(Peven), IFFT_re(Podd)

    # setup the IFFT list of values
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

def IFFT(P: list):
    n = len(P)
    return [Yval/n for Yval in IFFT_re(P)]
