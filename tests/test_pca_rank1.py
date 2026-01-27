import pytest
import numpy as np
# Updated import to reflect the package structure
from radiative_rigidity_pca.radiative_rigidity_pca import covariance, is_rank1

def test_perfect_rank1():
    """
    S0 Witness: Verifies that a mathematically pure rank-1 
    correlation matrix is identified correctly by the rigidity logic.
    """
    # Construct a deterministic rank-1 matrix
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
    
    # Introduce noise that exceeds the structural gap
    noisy_data = pure_data + np.eye(3) * 0.5
    
    # Should fail the rank-1 rigidity test
    assert is_rank1(noisy_data) is False

if __name__ == "__main__":
    pytest.main()
