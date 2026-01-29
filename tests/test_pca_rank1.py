import os
import sys
import numpy as np

# Ensure repo root is on sys.path so `import pca` works in CI
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pca import is_rank1


def test_is_rank1_true_on_rank1_matrix():
    # rank-1: outer product
    u = np.array([1.0, 2.0, 3.0])
    v = np.array([4.0, 5.0])
    data = np.outer(u, v)
    assert bool(is_rank1(data)) is True


def test_is_rank1_false_on_noisy_rank1_matrix():
    u = np.array([1.0, 2.0, 3.0])
    v = np.array([4.0, 5.0])
    data = np.outer(u, v)

    rng = np.random.default_rng(0)
    noisy_data = data + 1e-2 * rng.standard_normal(size=data.shape)
    assert bool(is_rank1(noisy_data)) is False
