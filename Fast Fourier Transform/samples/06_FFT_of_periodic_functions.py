from fast_fourier_transform import *
from math import exp, pi, sin, degrees
from cmath import phase
from numpy import linspace
import matplotlib.pyplot as plt


# The results in sample #03 suggest the following conjecture:
#           All periodic functions with integer frequencies have power spectra that consist only of spikes
#           at certain integer frequencies.

# The code below shows a few more examples to demonstrate, but not prove, the above conjecture.

def f_parabola(x, f):
    period = 1 / f
    phase = 5*((x % period) / period)
    value = -phase**2 + 2*phase + 4
    return value

def f_cubic(x, f):
    period = 1 / f
    phase = 4*((x % period) / period)
    value = phase**3 - 6*phase**2 + 9*phase - 2
    return value

def f_exposin(x, f):
    period = 1 / f
    phase = pi*((x % period) / period)
    value = 5*exp(-phase)*(sin(phase))**2
    return value

def constant(x, c):
    return c

def f_nessound(x, f):
    period = 1 / f
    phase = (x % period) / period
    value = waveform_square(phase, 1, 1) + waveform_sawtooth_up(phase, 3, 1)
    return value


n = 2**10

waves = [('Constant', lambda x: constant(x, 5)),
         ('Parabola', lambda x: f_parabola(x, 15)),
         ('Cubic', lambda x: f_cubic(x, 15)),
         ('Exponential * Sine', lambda x: f_exposin(x, 15)),
         ('Square + Sawtooth', lambda x: f_nessound(x, 15))]



for waveName, waveFunc in waves:
    print(f"-----{waveName}-----")
    input("")
    print("")

    # setup the physical domain (x, y)
    xRange = linspace(0, 1, n)
    yRange = [waveFunc(x) for x in xRange]

    # setup the frequency domain (f, u) by getting the Discrete Fourier Transform of yRange and getting the magnitudes
    # of each value
    fRange = list(range(n))
    uRange = FFT(yRange)
    uAbs = [abs(u) for u in uRange]     # this is data for what is called a Power Spectrum
    uPhase = [degrees(phase(u)) for u in uRange]

    # find where there are spikes in the magnitudes of the Fourier Transforms and print at which frequency do they
    # occur and what fractions are their heights relative to the highest spike
    maxU = max(uAbs)
    threshold = maxU / 20    # take spikes that have a height above 5% of the highest spike
    spikePoints = [(f, uAbs/maxU) for f, uAbs in zip(fRange, uAbs) if uAbs >= threshold]
    fSpikes = [point[0] for point in spikePoints]
    uSpikes = [round(point[1], 3) for point in spikePoints]
    print(f"Spike Frequencies:  {fSpikes}")
    print(f"Spike Heights:   {uSpikes}")
    input("")

    # plot the wave and its Discrete Fourier Transform (Power Spectrum)
    fig, axis = plt.subplots(2)
    fig.suptitle(f'{waveName} and DFT')
    axis[0].plot(xRange, yRange)
    axis[0].set(xlabel = "x", ylabel = "Y(x)")
    axis[1].plot(fRange[:n//2], uAbs[:n//2])
    axis[1].set(xlabel = "f", ylabel = "|U(f)|")
    print(uRange[0])
    plt.show()


    # calculate the inverse transform to get back the original function
    yInvRange = IFFT(uRange)
    fig, axis = plt.subplots(1)
    fig.suptitle(f'{waveName} generated from IFFT')
    axis.plot(xRange, yRange, 'tab:orange')
    axis.plot(xRange, yInvRange, 'tab:blue')
    axis.set(xlabel = "x", ylabel = "Y(x)")
    plt.show()