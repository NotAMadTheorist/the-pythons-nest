from numpy import dot

def projection_hyperplane(XPoint, A, b):
    """Finds the orthogonal projection X of XPoint on the hyperplane formed by the equation dot(A, X) = b,
    where XPoint, X, and A are vectors in n-space and b is a scalar."""

    projectionFactor = (b - dot(XPoint, A)) / dot(A, A)
    projectionX = XPoint + projectionFactor*A
    return projectionX