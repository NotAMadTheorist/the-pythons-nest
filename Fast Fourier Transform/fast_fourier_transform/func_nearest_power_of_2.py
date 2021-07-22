
def nearest_power_of_2(n:int, isInclusive:bool=True):
    """Returns the lowest power of 2 that is at least (or greater than if isInclusive=False) the given positive
    integer n."""

    if n < 1:
        raise Exception(f"Expected to receive a positive integer. Received {n}.")

    powerOf2 = 1
    while powerOf2 < n:
        powerOf2 *= 2

    return powerOf2