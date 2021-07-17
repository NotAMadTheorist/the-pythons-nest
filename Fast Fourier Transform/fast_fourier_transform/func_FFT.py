# reference:  https://www.youtube.com/watch?v=h7apO7q16V0

from cmath import rect, pi
from math import log2

def FFT_calc(Y: list):
    """Calculates the discrete fourier transform recursively using the Fast Fourier Transform (FFT) algorithm.
    """

    # set n to be the number of values in Y
    n = len(Y)

    # if n is 1, simply return Y (base case)
    if n == 1:
        return Y

    # compute omega  e**(-2*pi*j / n),  which is 2*pi/n radians along the unit circle in the clockwise
    # direction
    w = rect(1, -2*pi/n)


    # Split Y into even and odd parts with half the size of Y to introduce positive-negative pairs
    Yeven, Yodd = Y[::2], Y[1::2]

    # In the polynomial view, this just means to factor an (n-1)th degree polynomial Y[n-1](x) into polynomials
    # with degree ((n-1)/2 - 1) in the following manner:
    #       Y[n-1](x) =  Yeven[(n-1)/2 - 1](x) + x * Yodd[(n-1)/2 - 1](x)

    # perform FFT on the smaller range of numbers, or evaluate the values of Yeven and Yodd at even powers of w
    # from 1, w**2, w**4, ... w**n (recursive step)
    Ueven, Uodd = FFT_calc(Yeven), FFT_calc(Yodd)

    # setup the FFT list of values
    U = [0]*n

    # loop through each of the n//2 pairs of n complex inputs around the unit circle
    for k in range(n//2):
        # k represents each pair of positive-negative points on the unit circle in the complex plane
        # For the polynomial viewpoint, where we began with coefficients of Y(x), we substitute x = w**k.

        # get the kth values from the even and odd parts
        # In the polynomial viewpoint, this can be interpreted as evaluating the two addends in the formula:
        #       Y[n-1](x) =  Yeven[(n-1)/2 - 1](x) + x * Yodd[(n-1)/2 - 1](x)
        evenPart = Ueven[k]
        oddPart = w**k * Uodd[k]

        # A property of positive-negative pairs allows us to get two function values by simply changing one
        # operation.
        U[k] = evenPart + oddPart
        U[k + n//2] = evenPart - oddPart

        # Here mathematically, U[k + n//2] is equivalent to U[-k], since negating a complex number on the unit
        # circle corresponds to rotating it by pi radians or 180 degrees about the circle

    return U

def FFT(Y: list):
    """Computes the discrete fourier transform at each value of Y given that Y has a length "n" equivalent to a power
        of 2 (so n = 1, 2, 4, 8, 16, 32, and so on).

        ======

        ANALOGIES:
            It is equivalent to translating between physical domain (space or time) in the variables x or t,
          and frequency domain in the variable q.

           It is also equivalent to converting coefficients of an (n-1)th degree polynomial to function
          values obtained by evaluating the polynomial on n complex numbers spaced around the unit circle in
          the complex plane.

        ======

        RANGE OF INPUTS AND OUTPUTS
          If the inputs of the FFT are y-coordinates of n points in the physical xy or ty plane, then the
          x-coordinates or times are n equally spaced numbers on the interval [0, s] inclusive of boundaries,
          where s is any arbitrary scaling factor which may be set to describe a physical property.

          The outputs of the FFT are the complex Fourier Transform values, represented by the
          variable u, of frequency values f (which is in Hertz if x is in seconds) which are equally
          spaced numbers on the interval [0, (2**n - 1)/s].

        ===


        CHANGING RANGES
          Shrinking the range for the physical variable x or t expands the frequency range for f but also
          expands the gap between two frequency values.

          Expanding the range for the physical variable x or t shrinks the frequency ranges but
          decreases the gap between two frequency values.

          Increasing n to a higher power of 2 does not change the range of the physical variable,
          but it does expand the range of the frequency values while preserving the gaps between
          frequencies.
        """

    # check if the length of Y is a power of 2
    n = len(Y)
    isPowerof2 = True
    quotient = n
    while quotient > 1:
        quotient, remainder = quotient // 2, quotient % 2
        if remainder != 0:
            isPowerof2 = False
            break

    if not isPowerof2:
        raise Exception(f"Fast Fourier Transform works only for arrays with a length equivalent to a power of 2. "
                        f"Recieved array of length {n} = 2**{log2(n):.2f}.")

    # simply return the discrete fourier transform of Y
    return FFT_calc(Y)




