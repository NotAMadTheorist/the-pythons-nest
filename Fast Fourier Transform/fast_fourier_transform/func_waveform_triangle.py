def waveform_triangle(x, frequency, amplitude = 1):
    period = 1 / frequency
    phaseValue = ((x / period) % 1) * 4
    if phaseValue in [0, 2]:
        return 0
    elif phaseValue == 1:
        return amplitude
    elif phaseValue == 3:
        return -amplitude
    elif phaseValue < 1:
        return phaseValue * amplitude
    elif phaseValue < 3:
        return (2 - phaseValue) * amplitude
    else:
        return -(4 - phaseValue) * amplitude
