import numpy as np

def covariance(D: np.ndarray) -> np.ndarray:
    D = np.asarray(D, dtype=float)
    if D.ndim != 2:
        raise ValueError("covariance expects a 2D array")
    if D.shape[0] == 0:
        raise ValueError("covariance expects at least one observation")
    if D.shape[1] == 0:
        raise ValueError("covariance expects at least one feature")
    if not np.isfinite(D).all():
        raise ValueError("covariance expects finite values")
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
    if not np.isfinite(C).all():
        raise ValueError("is_rank1 expects finite values")
    if not np.isfinite(rtol) or rtol < 0:
        raise ValueError("rtol must be finite and nonnegative")
    if not np.isfinite(atol) or atol < 0:
        raise ValueError("atol must be finite and nonnegative")
    if C.shape[0] == 0 or C.shape[1] == 0:
        raise ValueError("is_rank1 expects non-empty dimensions")
    s = np.linalg.svd(C, compute_uv=False)
    if s.size <= 1:
        return True
    return float(s[1]) <= atol + rtol * float(s[0])
