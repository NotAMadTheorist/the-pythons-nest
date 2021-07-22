
def pad_zeros(alist: list):
    """Adds zeroes to the end of the list of numbers such that its length is a power of 2."""
    alist2 = alist.copy()

    # search for the lowest power of 2 that is at least the length of the list
    n = len(alist2)
    powerOf2 = 1
    while powerOf2 < n:
        powerOf2 *= 2

    if powerOf2 == n:
        return alist2

    # check types of numbers in alist
    valueTypes = set([type(value) for value in alist])
    if complex in valueTypes:
        zero = 0+0j
    elif float in valueTypes:
        zero = 0.0
    else:
        zero = 0

    # append zeros to the end of alist2
    alist2.extend([zero]*(powerOf2 - n))
    return alist2