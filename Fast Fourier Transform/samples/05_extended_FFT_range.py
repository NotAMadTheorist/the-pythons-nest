
# Reference:  https://jackschaedler.github.io/circles-sines-signals/index.html

# We can actually take the FFT of signals even if they are not ordinates in the physical range [0, 1].
# Again, we'll assume the physical function Y(x) has Fourier Transform U(f)
# Notice that we sample the signal Y(x) at discrete points - each element in our input list is a sample
#
# Main Parameters:
#   a.  Sampling Rate in x  --- number of samples you make per unit of x
#   b.  Sampling Range in x --- length of x units where samples are taken
#   c.  n of samples ---------- total number of samples taken
#
# Equations:
#   a.  (sampling rate in x)   =  (n of samples) / (sampling range in x)
#   b.  (sampling gap in x)    =  (sampling range in x) / (n of samples)   =  1  /  (sampling rate in x)
#   c.  (sampling range in f)  =  (sampling rate in x)
#   d.  (nyquist f)            =  (sampling rate in x) / 2
#   e.  (sampling gap in f)    =  (sampling range in f) / (n of samples)   =  1 / (sampling range in x)
#
# In other words:
#     sampling rate  =   n of samples  /  sampling range
#     sampling gap   =   sampling range  /  sampling range


# Importing packages
from math import cos, pi, exp
from fast_fourier_transform import FFT, IFFT, pad_zeros, nearest_power_of_2, waveform_square
import matplotlib.pyplot as plt

# For example, if we have the following signals:
samplingRate = 8192
startingX = 0

signals = [("440 Hz Square Wave", lambda x: waveform_square(x, 440, 1)),
           ("440 Hz Sine Wave", lambda x: cos(2*pi*x*440))]

for name, signalY in signals:
    for samplingRangeX in [1, 3, 4]:
        samplingGapX = 1 / samplingRate
        nOfSamples = samplingRate * samplingRangeX
        nPadded = nearest_power_of_2(nOfSamples)
        xRange = [startingX + k*samplingGapX for k in range(nOfSamples)]
        yRange = [signalY(x) for x in xRange]
        xRange = [startingX + k*samplingGapX for k in range(nPadded)]
        yRange = pad_zeros(yRange)

        samplingRangeF = samplingRate
        nyquistF = samplingRate // 2
        samplingGapF = 1 / samplingRangeX
        fRange = [k*samplingGapF for k in range(nPadded)]
        uRange = FFT(yRange)
        uAbsRange = [abs(u) for u in uRange]

        # plot only frequencies below the Nyquist Frequency since the other side of the graph is simply a
        # reflection of the side shown here.
        fig, axis = plt.subplots(1)
        fig.suptitle(f"Fourier Transform of a {name} from x = 0 to x = {samplingRangeX}")
        axis.plot(fRange[:int(nyquistF/samplingGapF)], uAbsRange[:int(nyquistF/samplingGapF)])
        plt.show()

# Only the heights of the spikes seem to change as we increase the range of x; as the range of x increases, the
# heights of the spikes become larger, but the overall distribution of frequencies still stays the same.

# Note that while zero padding allows us to have sampling ranges that are not powers of 2, leakage still occurs
# to an extent in these cases since we can observe that the spikes are wider when the range is 3.
