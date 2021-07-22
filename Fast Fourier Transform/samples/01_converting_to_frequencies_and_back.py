from fast_fourier_transform import *
from numpy import linspace
import matplotlib.pyplot as plt
from cmath import sin

# if the inputs of the FFT are y-coordinates then the x-coordinates are simply equally spaced numbers on the
# interval [0, s], where s is an arbitrary scaling factor

# then the output of the FFT are frequency values (in Hertz if x-coordinates are seconds) that are equally spaced
# on the interval [0, (2**n - 1)/s].

# In this case, we have s = 1, so the FFT translates from y-values on an x-interval [0, 1] to complex fourier
# values on a frequency interval [0, 2**n - 1]. The IFFT does the reverse process.

# parameters
k = 8
n = 2**k


# function to evaluate
Y = lambda x: sin(2*pi*x*13) + sin(2*pi*x*25)

xVals = linspace(0, 1, n)
yVals = [Y(x) for x in xVals]


# show graph of original function
plt.plot(xVals, yVals)
plt.show()


# take the fourier transform of f(x)
fVals = [f for f in range(n)]
uVals = FFT(yVals)
uMagnitudes = [abs(u) for u in uVals]   # what we are plotting here is also called a Power Spectrum


# show the magnitudes of the fourier transform
plt.plot(fVals[:35], uMagnitudes[:35])
plt.show()


# if the inputs of the IFFT are frequency values (in Hertz if x-coordinates are seconds) that are equally spaced
# on the interval [0, (2**n - 1)/s],
#
# then the output of the IFFT are y-coordinates whose x-coordinates are simply equally spaced numbers on the
# interval [0, s], where s is an arbitrary scaling factor


# take the inverse fourier transform to get back the original function
yValsComplex = IFFT(uVals)
newYVals = [y.real for y in yValsComplex]


# show the reconstructed original function
plt.plot(xVals, newYVals)
plt.show()

# I should get back the original function