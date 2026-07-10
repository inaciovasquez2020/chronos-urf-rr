import numpy as np

def covariance(D: np.ndarray) -> np.ndarray:
    D = np.asarray(D, dtype=float)
    if D.ndim != 2:
        raise ValueError("covariance expects a 2D array")
    if D.shape[0] == 0:
        raise ValueError("covariance expects at least one observation")
    if D.shape[1] == 0:
        raise ValueError("covariance expects at least one feature")
    mu = D.mean(axis=0, keepdims=True)
    X = D - mu
    return (X.T @ X) / max(1, X.shape[0])

def is_rank1(
    C: np.ndarray,
    *,
    rtol: float = 1e-7,
    atol: float = 1e-12,
) -> bool:
    C = np.asarray(C, dtype=float)
    if C.ndim != 2:
        raise ValueError("expected a 2D array")
    s = np.linalg.svd(C, compute_uv=False)
    if s.size <= 1:
        return True
    return float(s[1]) <= atol + rtol * float(s[0])
