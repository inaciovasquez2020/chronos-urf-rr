import numpy as np

def gf2_nullspace_basis(A):
    A = A.copy()
    rows, cols = A.shape
    r = 0
    pivots = []
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if A[i, c]:
                pivot = i
                break
        if pivot is None:
            continue
        A[[r, pivot]] = A[[pivot, r]]
        for i in range(rows):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        pivots.append(c)
        r += 1
        if r == rows:
            break

    free_cols = [c for c in range(cols) if c not in pivots]
    basis = []

    for free in free_cols:
        v = np.zeros(cols, dtype=np.uint8)
        v[free] = 1
        for i, pivot_col in reversed(list(enumerate(pivots))):
            if A[i, free]:
                v[pivot_col] = 1
        basis.append(v)

    return basis

def hamming_weight(v):
    return int(np.sum(v))
