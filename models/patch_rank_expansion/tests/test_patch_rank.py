from models.patch_rank_expansion.patch_rank_expansion import (
    random_k_sat_matrix,
    patch_rank_density,
)

def test_rank_density_bounds():
    A = random_k_sat_matrix(50, 80, 3)
    densities = patch_rank_density(A, 1)
    for d in densities:
        assert 0.0 <= d <= 1.0

def test_nontrivial_rank():
    A = random_k_sat_matrix(60, 90, 3)
    densities = patch_rank_density(A, 2)
    assert max(densities) > 0.1
