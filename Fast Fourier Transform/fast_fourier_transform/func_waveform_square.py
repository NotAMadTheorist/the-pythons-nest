def waveform_square(x, frequency, amplitude = 1):
    period = 1 / frequency
    phaseValue = (x / period) % 1
    if phaseValue in [0, 0.5]:
        return 0
    elif phaseValue < 0.5:
        return amplitude
    elif phaseValue > 0.5:
        return -amplitude
