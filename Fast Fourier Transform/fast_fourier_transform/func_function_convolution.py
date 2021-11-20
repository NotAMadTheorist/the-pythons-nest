from fast_fourier_transform.func_FFT import *
from fast_fourier_transform.func_IFFT import *

def function_convolution(Y1:list, Y2:list, scaleToOne=True, typeCheck:bool=True):
    """Returns the values of the convolution function Y1 ⨂ Y2 of two functions whose values on the interval
    [0, 1] are the inputs Y1 and Y2. Requires Y1 and Y2 to have the same number of entries. Scales down output
    between -1 and 1 by default as the original values are too large to graph."""

    if len(Y1) != len(Y2):
        raise Exception(f"Expected Y1 and Y2 to have the same number of entries; received {len(Y1)} and {len(Y2)}"
                        f"entries, respectively.")

    returnFloatOutputs = False
    if typeCheck:
        # check which types are in the function values to determine which type are the output values going to be
        valueTypes = [type(y1) for y1 in Y1]
        valueTypes.extend([type(y2) for y2 in Y2])
        setOfTypes = set(valueTypes)
        if complex in setOfTypes:
            pass
        elif float in setOfTypes:
            returnFloatOutputs = True


    U1, U2 = FFT(Y1), FFT(Y2)
    U3 = [u1*u2 for u1, u2 in zip(U1, U2)]
    Y3 = IFFT(U3)

    if returnFloatOutputs:
        Y3 = [y3.real for y3 in Y3]

    if scaleToOne:
        maxMagnitude = max(abs(y) for y in Y3)
        Y3 = [y / maxMagnitude for y in Y3]

    return Y3
