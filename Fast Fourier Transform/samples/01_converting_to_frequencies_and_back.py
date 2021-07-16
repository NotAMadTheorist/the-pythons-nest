from fast_fourier_transform import *

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
f = lambda x: sin(2*pi*x*13) + sin(2*pi*x*25)

xVals = linspace(0, 1, n)
yVals = [f(x) for x in xVals]


# show graph of original function
plt.plot(xVals, yVals)
plt.show()


# take the fourier transform of f(x)
freqVals = [f for f in range(n)]
fourierVals = FFT(yVals)
fourierMags = [abs(F) for F in fourierVals]


# show the magnitudes of the fourier transform
plt.plot(freqVals, fourierMags)
plt.show()


# if the inputs of the IFFT are frequency values (in Hertz if x-coordinates are seconds) that are equally spaced
# on the interval [0, (2**n - 1)/s],
#
# then the output of the IFFT are y-coordinates whose x-coordinates are simply equally spaced numbers on the
# interval [0, s], where s is an arbitrary scaling factor


# take the inverse fourier transform to get back the original function
yValsComplex = IFFT(fourierVals)
newYVals = [y.real for y in yValsComplex]


# show the reconstructed original function
plt.plot(xVals, newYVals)
plt.show()

# I should get back the original function