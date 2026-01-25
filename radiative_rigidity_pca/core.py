import numpy as np

def covariance(D: np.ndarray) -> np.ndarray:
    D = np.asarray(D, dtype=float)
    mu = D.mean(axis=0, keepdims=True)
    X = D - mu
    return (X.T @ X) / max(1, X.shape[0])

def is_rank1(C: np.ndarray, tol: float = 1e-10) -> bool:
    s = np.linalg.svd(C, compute_uv=False)
    if s.size == 0:
        return True
    return (s[1] if s.size > 1 else 0.0) <= tol * (s[0] if s[0] > 0 else 1.0)
