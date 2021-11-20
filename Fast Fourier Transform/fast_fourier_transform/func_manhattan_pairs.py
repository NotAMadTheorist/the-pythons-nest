def manhattan_pairs(d: int):
    k = d
    while k >= 0:
        yield (k, d - k)
        k -= 1