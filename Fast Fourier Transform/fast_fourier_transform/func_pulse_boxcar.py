
def pulse_boxcar(x, startingX, width, amplitude=1):
    """Returns the value of a boxcar function with a given amplitude; returns (amplitude) whenever:
       startingX < x < startingX + width, returns (amplitude)/2 if x is at either boundary, and
       returns 0 otherwise."""

    endingX = startingX + width
    if x in [startingX, endingX]:
        return amplitude/2
    elif x < startingX:
        return 0
    elif x > endingX:
        return 0
    else:
        return amplitude