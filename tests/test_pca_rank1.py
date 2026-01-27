import numpy as np
from radiative_rigidity_pca.radiative_rigidity_pca import covariance, is_rank1

def test_rank1_synthetic():
    rng = np.random.default_rng(0)
    m, d = 100, 4
    u = rng.normal(size=(m, 1))
    v = rng.normal(size=(1, d))
    D = u @ v
    C = covariance(D)
    assert is_rank1(C, tol=1e-12)
