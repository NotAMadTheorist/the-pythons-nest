from numpy import dot

def projection_hyperplane(XPoint, A, b):
    """Finds the point in Rn on the hyperplane formed by the equation dot(A, x) = a1*x1 + a2*x2 + .. + an*xn = b that
    is closest to XPoint. Assumes all inputs are 1 dimensional arrays.

    In other words, it finds the orthogonal / perpendicular projection of XPoint on the hyperplane in Rn."""

    """Finds the orthogonal projection X of XPoint on the hyperplane formed by the equation dot(A, X) = b,
    where XPoint, X, and A are vectors in n-space and b is a scalar."""

    projectionFactor = (b - dot(XPoint, A)) / dot(A, A)
    projectionX = XPoint + projectionFactor*A
    return projectionX