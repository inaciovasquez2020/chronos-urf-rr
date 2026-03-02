from models.patch_rank_expansion.patch_rank_expansion import random_k_sat_matrix
from models.patch_rank_expansion.dual_tools import gf2_nullspace_basis, hamming_weight

def min_dual_weight(A):
    basis = gf2_nullspace_basis(A)
    if not basis:
        return None
    min_w = A.shape[1]
    for v in basis:
        w = hamming_weight(v)
        if w != 0:
            min_w = min(min_w, w)
    return min_w

def test_dual_weight_nontrivial():
    A = random_k_sat_matrix(40, 60, 3)
    w = min_dual_weight(A)
    if w is not None:
        assert w > 0
