import numpy as np
import pytest

from radiative_rigidity_pca import covariance, is_rank1


def test_package_is_rank1_accepts_outer_product_matrix():
    u = np.array([1.0, 2.0, 3.0])
    v = np.array([4.0, 5.0])
    assert is_rank1(np.outer(u, v))


def test_package_is_rank1_rejects_rank2_identity_matrix():
    assert not is_rank1(np.eye(2))


def test_package_is_rank1_rejects_non_2d_input():
    with pytest.raises(ValueError, match="2D"):
        is_rank1([1.0, 2.0, 3.0])


def test_package_covariance_matches_numpy_rowvar_false():
    x = np.array(
        [
            [1.0, 2.0],
            [3.0, 4.0],
            [5.0, 6.0],
        ]
    )
    np.testing.assert_allclose(covariance(x), np.cov(x, rowvar=False, bias=True))

def test_package_is_rank1_uses_absolute_tolerance_at_small_scale():
    matrix = np.diag([1e-12, 5e-13])
    assert is_rank1(matrix)

def test_package_covariance_rejects_non_2d_input():
    with pytest.raises(ValueError, match="2D"):
        covariance([1.0, 2.0, 3.0])
