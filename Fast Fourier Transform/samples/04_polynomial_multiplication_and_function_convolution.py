from fast_fourier_transform import *
from math import exp, pi, sin
from numpy import linspace
import matplotlib.pyplot as plt


# -------------------------- MATRIX MULTIPLICATION USING FFT AND IFFT -------------------------------------------

# Suppose we want to multiply two 7th degree polynomials:
#   P1(x) = 3 - x + 3x^2 - 7x^3 + 0x^4 + 6x^5 + 7x^6 + 7x^7
#   P2(x) = 5 - 3x - 3x^2 + 7x^3 - 5x^4 + x^5 + 0x^6 - x^7
P1 = [3, -1, 3, -7, 0, 6, 7, 7]
P2 = [5, -3, -3, 7, -5, 1, 0, -1]

# We can compute the product through lattice multiplication:
PProduct = multiply_polynomials_lattice(P1, P2)
print(f"Product from Lattice Method:  {PProduct}")

# But this process has algorithmic time O(n^2), meaning that if we had 10 times more coefficients, the number of
# computations, and therefore the time taken to output the product would increase by 100-fold.


# So is there another way to get the product more efficiently?
# One way is to evaluate both polynomials on 7+1 = 8 distinct values of x to get 8 points, multiply the respective
# y-coordinates, then find the interpolating polynomial, which can be proved to be unique.
#
# This simplifies the middle step greatly, however, if we limit ourselves to real values for x, evaluation and
# interpolation would also take time of O(n^2), since matrix computation is involved.


# As detailed in this video (https://www.youtube.com/watch?v=h7apO7q16V0), this can be circumvented by allowing
# the values of x to be n evenly spaced complex numbers on the unit circle of the complex plane, and taking
# advantage of the fact that an "n"th degree polynomial can be separated into two polynomials of about half
# the original degree by separating the odd coefficients and even coefficients. Given that we compute the values
# of those smaller polynomials first, we can get function values at distinct points by plugging in pairs of
# x-values: x and -x, with a few simple operations.
#
# This gives rise to the recursive algorithm called the Fast Fourier Transform (FFT), which can also be interpreted
# as translating polynomial coefficients to the values of the polynomial on the n complex numbers on the unit
# circle. With the FFT and its inverse, IFFT, we can find the polynomial product more efficiently through the
# alternative process of evaluation, multiplication, and interpolation, as this gives the product in O(n*log(n))
# time, rather than O(n^2).

# Now we try to multiply the polynomials through the FFT and IFFT as outlined in the video:

# We must pad the polynomials with 8 additional zeroes first so that the FFT has 16 entries, which is more
# than enough to cover 15 terms for the product:
P1.extend([0]*8)
P2.extend([0]*8)

# Then we translate to polynomial values using the FFT:
P1Values = FFT(P1)
P2Values = FFT(P2)

# Next, we multiply the 16 polynomial values to carry out the multiplication.
PProductValues = [p1*p2 for p1, p2 in zip(P1Values, P2Values)]

# Finally, we translate the polynomial values to the coefficients of the interpolating polynomial for the 16
# points in complex space, resulting in the product:
PProductFFT = IFFT(PProductValues)

# We round them to real integers since all our input coefficients are also real integers:
PProductFFT = [round(pprod.real) for pprod in PProductFFT]

# we remove one zero, resulting in the same coefficients:
PProductFFT.pop()
print(f"Product from FFT and IFFT:  {PProductFFT}")


# For ease of execution, there is a function on polynomial multiplication with FFT in this module to do all these
# steps in one call:

P1 = [3, -1, 3, -7, 0, 6, 7, 7]
P2 = [5, -3, -3, 7, -5, 1, 0, -1]

print(f"Product from FFT and IFFT:  {multiply_polynomials_FFT(P1, P2)}")


# -------------------------- FUNCTION CONVOLUTION -------------------------------------------

# To multiply two polynomials, we had to take the FFT of their coefficients, multiply them, and take the IFFT to
# get the resulting product.
#
#     Polynomial 1   --->  FFT(P1) --┐
#                                    ├---->  FFT(P1)*FFT(P2)  ---------->  Polynomial 1 * Polynomial 2
#     Polynomial 2   --->  FFT(P2) --┘                            IFFT
#
#
# However, if we instead interpret our inputs as the values of two functions on the interval [0, 1] and applied
# the same procedure, how would we interpret the output?

# The answer is that the outputs will be the function values of the CONVOLUTION, written as f(x)⨂ g(x), for the
# two selected functions f(x) and g(x) we associate our input values with. This is an operation on two functions
# which produces a third function that "blends" the graph of the first function with the second.

# This is a fact derived from the CONVOLUTION THEOREM, which states that for any three functions f(x), g(x),
# and h(x):
#     If   FFT(h) = FFT(f) * FFT(g),      then   h(x) = f(x) ⨂ g(x)


# For example, say we had two functions F1(x) and F2(x), the second of which has a value from 0 to 1 on the
# interval [0, 1], and we plot their convolution C(x) = F1(x) ⨂ F2(x).

# We have pairs of F1(x) and F2(x):

k = 12
n = 2**k

functions = [(lambda x: exp(-2*x), lambda x: pulse_boxcar(x, 0.2, 0.2)),
             (lambda x: exp(-2*x), lambda x: pulse_triangle(x, 0.3, 0.4)),
             (lambda x: pulse_boxcar(x, 0.25, 0.5), lambda x: pulse_boxcar(x, 0, 0.1)),
             (lambda x: pulse_boxcar(x, 0.25, 0.7), lambda x: exp(-64*(x-0.25)**2),),
             (lambda x: pulse_boxcar(x, 0.25, 0.5), lambda x: pulse_triangle(x, 0, 0.25)),
             (lambda x: waveform_square(x, 4, 0.3) + 0.3,  lambda x: exp(-8*x))]

for F1, F2 in functions:
    xRange = list(linspace(0, 1, n))
    y1Range = [F1(x) for x in xRange]
    y2Range = [F2(x) for x in xRange]
    ycRange = function_convolution(y1Range, y2Range)   # note that this is by default scaled between -1 and 1

    fig, axis = plt.subplots(1)
    fig.suptitle("Functions Y1(x) and Y2(x)")
    axis.plot(xRange, y1Range, 'tab:green')
    axis.plot(xRange, y2Range, 'tab:orange')
    axis.set(xlabel = 'x', ylabel = 'Y(x)')
    plt.show()

    fig, axis = plt.subplots(1)
    fig.suptitle("Scaled Convolution Function Y1(x) ⨂ Y2(x)")
    axis.plot(xRange, y1Range, 'tab:green', linestyle = 'dotted')
    axis.plot(xRange, y2Range, 'tab:orange', linestyle = 'dotted')
    axis.plot(xRange, ycRange, 'tab:blue')
    axis.set(xlabel = 'x', ylabel = 'Y(x)')
    plt.show()

# Notice that for the first pair of functions, the graph of the convolution has a similar shape to the falling
# exponential F1(x) but F2(x) causes the function to suddenly rise in the range [0.2, 0.4], as if the graphs
# were blended together.


