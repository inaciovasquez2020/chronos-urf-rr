def invariant(x):
    return x

def spec(x, v):
    return v == x

def check_invariant(x):
    v = invariant(x)
    return spec(x, v)
