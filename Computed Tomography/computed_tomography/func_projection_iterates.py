from computed_tomography.func_projection_hyperplane import *
from time import time

def projection_iterates(initialX, matrixA, vectorB, iterations, returnMultipleIterates:bool = False):
    """Repeatedly transforms the vector initialX in N-space by sequentially projecting it onto the M hyperplanes each
    formed by the equation dot(A, X) = a1*x1 + a2*x2 + ... + an*xn = b, where A is each row of matrixA and b is a value
    from vectorB. This process is done for a given number of iterations.

    Assumes initialX, matrixA, and vectorB are arrays and iterations is a positive integer.

    By default, it returns one vector resulting from applying all projections in all iterations.
    If returnMultipleIterates is set to True, it returns a list of M vectors representing the projection vectors
    obtained in the last iteration of the algorithm

    Each output vector can be interpreted as an approximate solution to the linear system matrixA * X = vectorB in
    M equations and N unknown variables."""

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

    time1 = time()
    print("Beginning projection algorithm")
    for p in range(iterations):
        time2 = time()
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
        time3 = time()
        timeIter = round(time3-time2, 3)
        print(f"Finished Iteration # {p + 1} out of {iterations} in {timeIter} s")
    time4 = time()
    timeTotal = round(time4 - time1, 3)

    print(f"Projection algorithm executed in {timeTotal} s \n")

    if not returnMultipleIterates:
        return currentX
    else:
        return recentIterates