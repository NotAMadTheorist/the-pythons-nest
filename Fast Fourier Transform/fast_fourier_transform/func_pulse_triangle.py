
def pulse_triangle(x, startingX, width, amplitude=1):
    """Returns the value of a triangular pulse at x."""

    endingX = startingX + width
    if x < startingX:
        return 0
    elif x > endingX:
        return 0

    phaseX = (x - startingX) / width * 2
    if phaseX < 1:
        return phaseX*amplitude
    elif phaseX == 1:
        return amplitude
    else:
        return (2 - phaseX) * amplitude