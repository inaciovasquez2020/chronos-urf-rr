import sys
import os
import pytest
import numpy as np

# Force local path inclusion so CI can find the 'radiative_rigidity_pca' folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Robust Import: Handles both 'folder.file' and direct 'module' structures
try:
    from radiative_rigidity_pca.radiative_rigidity_pca import covariance, is_rank1
except (ImportError, ModuleNotFoundError):
    try:
        from radiative_rigidity_pca import covariance, is_rank1
    except ImportError:
        # Fallback for local dev environments
        import radiative_rigidity_pca as rr
        covariance = rr.covariance
        is_rank1 = rr.is_rank1

def test_rank1_synthetic():
    """
    Verifies that generated rank-1 data is correctly identified.
    """
    rng = np.random.default_rng(0)
    m, d = 100, 4
    u = rng.normal(size=(m, 1))
    v = rng.normal(size=(1, d))
    D = u @ v
    C = covariance(D)
    assert is_rank1(C, tol=1e-12)

def test_perfect_rank1():
    """
    S0 Witness: Verifies that a mathematically pure rank-1 
    correlation matrix is identified correctly.
    """
    v = np.array([1.0, 2.0, 3.0])
    data = np.outer(v, v)
    
    # Structural check
    assert is_rank1(data) is True

def test_noisy_rigidity_wall():
    """
    S0 Witness: Verifies that noise exceeding the URF threshold
    breaks the rank-1 rigidity constraint.
    """
    v = np.array([1.0, 2.0, 3.0])
    pure_data = np.outer(v, v)
    
    # Introduce noise that exceeds the structural gap (Rigidity Wall)
    # This should cause the is_rank1 check to return False
    noisy_data = pure_data + np.eye(3) * 0.5
    
    assert is_rank1(noisy_data) is False

if __name__ == "__main__":
    pytest.main([__file__])
