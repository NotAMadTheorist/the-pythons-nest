def waveform_sawtooth_up(x, frequency, amplitude = 1):
    period = 1 / frequency
    phaseValue = ((x / period) % 1) * 2
    if phaseValue in [0, 1]:
        return 0
    else:
        return (phaseValue - 1) * amplitude
