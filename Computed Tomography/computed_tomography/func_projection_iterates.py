from computed_tomography.func_projection_hyperplane import *

def projection_iterates(initialX, matrixA, vectorB, iterations, returnMultipleIterates:bool = False):
    """Iterates the vector initialX in n-space by orthogonally projecting it onto the M hyperplanes represented by
    each equation of the system (matrixA)(X) = vectorB. Returns a set of M iterate vectors obtained from the final
    iteration of applying the procedure described."""

    # test whether the sizes of the inputs are valid
    vectorDimension = initialX.shape[0]
    numberOfEquations = matrixA.shape[0]
    isValidInput = (vectorDimension == matrixA.shape[1]) and (numberOfEquations == vectorB.shape[0])

    if not isValidInput:
        raise Exception(f"Expected matrixA to have size {numberOfEquations} x {vectorDimension} and vectorB to have"
                        f" size {numberOfEquations} x 1.")


    currentX = initialX
    recentIterates = []

    zeroRow = [0]*vectorDimension
    isZeroRow = lambda row: sum(row == zeroRow) == vectorDimension

    isLastIteration = False
    for p in range(iterations):
        if p == iterations - 1:
            isLastIteration = True
        for k in range(numberOfEquations):
            A = matrixA[k]
            if isZeroRow(A):
                continue

            b = vectorB[k]
            newX = projection_hyperplane(currentX, A, b)
            if isLastIteration:
                recentIterates.append(newX)
            currentX = newX

    if not returnMultipleIterates:
        return currentX
    else:
        return recentIterates