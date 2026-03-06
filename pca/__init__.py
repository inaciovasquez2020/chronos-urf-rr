import numpy as np

def is_rank1(x, *, rtol=1e-7, atol=1e-12) -> bool:
    a = np.asarray(x, dtype=float)
    if a.ndim != 2:
        raise ValueError("is_rank1 expects a 2D array")

    m, n = a.shape
    if m <= 1 or n <= 1:
        return True

    s = np.linalg.svd(a, compute_uv=False)
    s1, s2 = float(s[0]), float(s[1])
    return s2 <= (atol + rtol * s1)
