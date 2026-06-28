import numpy as np
import pytest

from pca import is_rank1


def test_is_rank1_accepts_outer_product_matrix():
    u = np.array([1.0, 2.0, 3.0])
    v = np.array([4.0, 5.0])
    assert is_rank1(np.outer(u, v))


def test_is_rank1_rejects_rank2_identity_matrix():
    assert not is_rank1(np.eye(2))


def test_is_rank1_rejects_non_2d_input():
    with pytest.raises(ValueError, match="2D array"):
        is_rank1([1.0, 2.0, 3.0])
