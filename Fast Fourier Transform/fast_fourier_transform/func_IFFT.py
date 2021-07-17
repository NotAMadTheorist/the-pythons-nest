# reference:  https://www.youtube.com/watch?v=h7apO7q16V0
from cmath import rect, pi
from math import log2

def IFFT_calc(U: list):
    """Calculates the inverse discrete fourier transform of U recursively using a slightly modified version of the
    Fast Fourier Transform (FFT) algorithm."""


    # set n to be the number of values in U
    n = len(U)

    # if n is 1, simply return U (base case)
    if n == 1:
        return U

    # compute omega = e**(2*pi*j / n),  which is 2*pi/n radians along the unit circle in the counter-clockwise
    # direction
    w = rect(1, 2*pi/n)

    # Split U into even and odd parts with half the size of U to introduce positive-negative pairs
    Ueven, Uodd = U[::2], U[1::2]

    # perform IFFT on the smaller range of numbers, or evaluate the values of Ueven and Uodd at even powers of w
    # from 1, w**2, w**4, ... w**n (recursive step)
    Yeven, Yodd = IFFT_calc(Ueven), IFFT_calc(Uodd)

    # setup the IFFT list of values
    Y = [0]*n

    # loop through each of the n//2 pairs of n complex inputs around the unit circle
    for k in range(n//2):
        # k represents each pair of positive-negative points on the unit circle in the complex plane
        # For the polynomial viewpoint, where we began with coefficients of P(x), we substitute x = w**k.

        evenPart = Yeven[k]
        oddPart = w**k * Yodd[k]

        # A property of positive-negative pairs allows us to get two function values by simply changing one
        # operation.
        Y[k] = evenPart + oddPart
        Y[k + n//2] = evenPart - oddPart

        # Here mathematically, Y[k + n//2] is equivalent to Y[-k], since negating a complex number on the unit
        # circle corresponds to rotating it by pi radians or 180 degrees about the circle

    return Y

def IFFT(U: list):
    """Computes the discrete inverse fourier transform at each value of U given that U has a length "n" equivalent
     to a power of 2 (so n = 1, 2, 4, 8, 16, 32, and so on).

        ======

        ANALOGIES:

        It is equivalent to translating from the frequency domain in the variable f to the physical domain
        (space or time) in the variables x or t.

        It is also equivalent to converting the function values of a polynomial on n complex numbers spaced
        around the unit circle in the complex plane to coefficients of an (n-1)th degree polynomial which
        interpolates them.

        ======

        RANGE OF INPUTS AND OUTPUTS

            If the inputs of the IFFT are the complex Fourier Transform values, represented by the variable u,
            then the corresponding frequencies f (which is in Hertz if x is in seconds) of those values are
            equally spaced numbers on the interval [0, p(2**n - 1)] inclusive of boundaries, where p is an
            arbitrary scaling factor that may be calibrated to fit the situation.

            The outputs of the IFFT are y-coordinates of n points in the physical xy or ty plane, whose
            x-coordinates or times are n equally spaced numbers on the interval [0, 1/p].
        ===


        CHANGING RANGES
            Shrinking the range for the frequency f expands the range for the physical variable x or t but also
            expands the gap between two x values or time values.

            Expanding the range for the frequency f shrinks the range of the physical variable x or t but
            decreases the gap between two x values or time values.

            Increasing n to a higher power of 2 expands the range of the frequency f, but does not change the
            range of the physical variable x or t.
        """

    # check if the length of U is a power of 2
    n = len(U)
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

    # simply return the discrete fourier transform of U
    return [Y/n for Y in IFFT_calc(U)]

