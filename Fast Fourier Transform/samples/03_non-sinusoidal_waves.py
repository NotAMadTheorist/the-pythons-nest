from fast_fourier_transform import *
from numpy import linspace
import matplotlib.pyplot as plt
from cmath import phase
from math import degrees


# Parameters
k = 10
n = 2**k

# Intro
print("Power Spectra of Non-Sinusoidal Waves")
input("")
print("")


# waves to analyze:
waveFrequency = 5
waves = [("Square Wave", lambda x: waveform_square(x, waveFrequency)),
         ("Triangle Wave", lambda x: waveform_triangle(x, waveFrequency)),
         ("Rising Sawtooth Wave", lambda x: waveform_sawtooth_up(x, waveFrequency)),
         ("Falling Sawtooth Wave", lambda x: waveform_sawtooth_down(x, waveFrequency)),
         ("Combined Signal", lambda x: waveform_square(x, waveFrequency) + waveform_square(x, waveFrequency*2)/4)]

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
    fig.suptitle(f'{waveName} and Discrete Fourier Transform')
    axis[0].plot(xRange, yRange)
    axis[0].set(xlabel = "x", ylabel = "Y(x)")
    axis[1].plot(fRange[:n//2], uAbs[:n//2])
    axis[1].set(xlabel = "f", ylabel = "|U(f)|")
    plt.show()

    # calculate the inverse transform to get back the original function
    yInvRange = IFFT(uRange)
    fig, axis = plt.subplots(1)
    fig.suptitle(f'{waveName} generated from IFFT')
    axis.plot(xRange, yRange, 'tab:orange')
    axis.plot(xRange, yInvRange, 'tab:blue')
    axis.set(xlabel = "x", ylabel = "Y(x)")
    plt.show()

#                                            ----------------------
# Notice that if we let the waveFrequency be f0, the spikes in the Fourier Transform of a square wave fall slowly
# and occur at the following frequencies:
#           f    =  f0,   3*f0,   5*f0,   7*f0,  ...  (2*k + 1)*f0,   where k is a positive integer
#
# Thus, we say that a square wave only has odd-numbered harmonics, that is, frequencies which make it up that are
# multiples of its fundamental frequency f0.
# If we take the reciprocal of the spike heights, these heights are in the following ratio:
#       heights   =  1,  1/3,  1/5,  1/7,  ...  1/(2*k + 1),          where k is a positive integer


#                                            ----------------------
# For the FT of a triangle wave, magnitudes of the spikes fall quickly, but the location of the spikes share the
# same pattern for a square wave; at odd-numbered harmonics.
# However, the heights of the spikes are now in the following ratio:
#       heights   =   1,  1/(3**2),    1/(5**2),   1/(7**2), ... 1/(2*k+1)**2,    where k is a positive integer


#                                            ----------------------
# However, the spikes in the FTs of sawtooth waves also fall slowly and occur more frequently:
#       f   =  f0,  2*f0,  3*f0,  4*f0, ...   k*f0,   where k is a positive integer
# and the magnitudes of the FTs for both waves are identical. What creates differing shapes for the sawtooth waves
# are instead the phases of the complex FTs.
# Since sawtooth waves have all integer harmonics, the spike heights now follow the ratio:
#      height:   1,   1/2,   1/3,   1/4,  ...   1/k,   where k is a positive integer

