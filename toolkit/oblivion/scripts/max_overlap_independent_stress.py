import itertools
import numpy as np

def rank_mod2(A):
    A = A.copy().astype(np.uint8)
    m, n = A.shape
    r = 0
    pivots = []
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if A[i, c]:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r:
            A[[r, pivot]] = A[[pivot, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        pivots.append(c)
        r += 1
        if r == m:
            break
    return r

def distinct_rows(A):
    return len({tuple(row.tolist()) for row in A})

def row_weights(A):
    return A.sum(axis=1)

def col_weights(A):
    return A.sum(axis=0)

def make_band_family(m, B):
    V = m + B - 1
    A = np.zeros((V, m), dtype=np.uint8)
    for j in range(m):
        A[j:j+B, j] = 1
    return A

def make_sliding_window_family(m, B, shift):
    V = shift * (m - 1) + B
    A = np.zeros((V, m), dtype=np.uint8)
    for j in range(m):
        s = j * shift
        A[s:s+B, j] = 1
    return A

def make_circulant_family(m, B):
    V = m
    A = np.zeros((V, m), dtype=np.uint8)
    for j in range(m):
        for t in range(B):
            A[(j + t) % V, j] = 1
    return A

def make_block_overlap_family(blocks, copies, B):
    V = blocks * B
    m = blocks * copies
    A = np.zeros((V, m), dtype=np.uint8)
    col = 0
    for b in range(blocks):
        base = b * B
        block_vertices = list(range(base, base + B))
        families = []
        for t in range(copies):
            vec = np.zeros(V, dtype=np.uint8)
            if t < B:
                vec[block_vertices] = 1
                vec[block_vertices[t]] = 0
            else:
                vec[block_vertices] = 1
            families.append(vec)
        for vec in families[:copies]:
            A[:, col] = vec
            col += 1
    return A[:, :col]

def filter_independent_columns(A):
    cols = []
    current = np.zeros((A.shape[0], 0), dtype=np.uint8)
    for j in range(A.shape[1]):
        candidate = np.concatenate([current, A[:, [j]]], axis=1)
        if rank_mod2(candidate) > rank_mod2(current):
            cols.append(j)
            current = candidate
    return A[:, cols]

def analyze(name, A, B=None, L=None):
    r = rank_mod2(A)
    m = A.shape[1]
    v = A.shape[0]
    u = distinct_rows(A)
    rw = row_weights(A)
    cw = col_weights(A)
    print(name)
    print("shape:", A.shape)
    print("rank:", r)
    print("rank/m:", 0 if m == 0 else r / m)
    print("distinct_rows:", u)
    print("min_row_wt:", int(rw.min()) if v else 0)
    print("max_row_wt:", int(rw.max()) if v else 0)
    print("min_col_wt:", int(cw.min()) if m else 0)
    print("max_col_wt:", int(cw.max()) if m else 0)
    if B is not None and L is not None and B * L > 0:
        print("threshold_m_over_BL:", m / (B * L))
    print()

def main():
    cases = []

    for m, B in [(40, 3), (60, 4), (80, 5)]:
        A = make_band_family(m, B)
        L = int(row_weights(A).max())
        cases.append((f"band_family_m{m}_B{B}", A, B, L))

    for m, B, shift in [(50, 4, 1), (50, 4, 2), (80, 5, 1), (80, 5, 2)]:
        A = make_sliding_window_family(m, B, shift)
        L = int(row_weights(A).max())
        cases.append((f"sliding_family_m{m}_B{B}_shift{shift}", A, B, L))

    for m, B in [(31, 3), (63, 5)]:
        A = make_circulant_family(m, B)
        A = filter_independent_columns(A)
        L = int(row_weights(A).max())
        cases.append((f"circulant_family_m{m}_B{B}", A, B, L))

    for blocks, copies, B in [(10, 3, 4), (12, 4, 5)]:
        A = make_block_overlap_family(blocks, copies, B)
        A = filter_independent_columns(A)
        L = int(row_weights(A).max())
        cases.append((f"block_overlap_blocks{blocks}_copies{copies}_B{B}", A, B, L))

    for name, A, B, L in cases:
        analyze(name, A, B, L)

if __name__ == "__main__":
    main()
