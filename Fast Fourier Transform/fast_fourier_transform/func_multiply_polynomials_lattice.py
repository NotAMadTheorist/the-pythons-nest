from fast_fourier_transform.func_manhattan_pairs import *

def multiply_polynomials_lattice(polynomial1:list, polynomial2:list):
    """Multiplies two polynomials given their coefficients in a list from lowest to highest degree through the
    lattice method and returns the coefficients of their product."""

    m, n = len(polynomial1), len(polynomial2)

    product = []
    for degree in range(m + n - 1):
        sumProduct = 0
        for i, j in manhattan_pairs(degree):
            if j < n and i < m:
                sumProduct += polynomial1[i]*polynomial2[j]
        product.append(sumProduct)

    return product

