from fast_fourier_transform import FFT, IFFT

def multiply_polynomials_FFT(polynomial1:list, polynomial2:list, typeCheck:bool = True):
    """Multiplies two polynomials given their coefficients in a list from lowest to highest degree by applying the
     Fast Fourier Transform (FFT) and the Inverse Fast Fourier Transform (IFFT). Returns the coefficients of their
     product."""

    # make a copy of the polynomials
    P1, P2 = polynomial1.copy(), polynomial2.copy()

    # get the length of each polynomial
    m, n = len(polynomial1), len(polynomial2)

    returnFloatOutputs = False
    returnIntegerOutputs = False
    if typeCheck:
        # check which types are in the polynomial to determine which type are the output coefficients going to be
        coeffTypes = [type(p1) for p1 in P1]
        coeffTypes.extend([type(p2) for p2 in P2])
        setOfTypes = set(coeffTypes)
        if complex in setOfTypes:
            pass
        elif float in setOfTypes:
            returnFloatOutputs = True
        else:
            returnIntegerOutputs = True


    # first get the lowest power of 2 that is at least the target value 2*max(m, n)
    target = 2*max(m, n)
    powerOf2 = 1
    while powerOf2 <= target:
        powerOf2 *= 2

    # pad the ends of each polynomial by zeroes such that their length is the chosen power of 2.
    P1.extend([0]*(powerOf2 - m))
    P2.extend([0]*(powerOf2 - n))

    # convert to values of the polynomial by evaluating it on equally spaced complex numbers on the unit circle
    # This is done recursively through the Fast Fourier Transform (FFT)
    P1Values = FFT(P1)
    P2Values = FFT(P2)

    # multiply the polynomial values together
    PProductValues = [p1Value * p2Value for p1Value, p2Value in zip(P1Values, P2Values)]

    # translate the polynomial values to the coefficients of the interpolating polynomial through the Inverse
    # Fast Fourier Transform (IFFT)
    PProductFFT = IFFT(PProductValues)

    # change the type of the product if all input entries are integers or floats
    if typeCheck:
        if returnIntegerOutputs:
            PProductFFT = [round(pprod.real) for pprod in PProductFFT]
        elif returnFloatOutputs:
            PProductFFT = [pprod.real for pprod in PProductFFT]

    # since the product has m + n - 1 terms, keep only the first m + n - 1 entries
    PProductFFT = PProductFFT[: (m + n - 1)]
    return PProductFFT
