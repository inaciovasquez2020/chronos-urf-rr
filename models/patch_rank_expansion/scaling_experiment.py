from models.patch_rank_expansion.patch_rank_expansion import random_k_sat_matrix
from models.patch_rank_expansion.dual_tools import gf2_nullspace_basis, hamming_weight
import numpy as np

def min_clause_dual_weight(A):
    AT = A.T
    basis = gf2_nullspace_basis(AT)
    if not basis:
        return None
    min_w = AT.shape[1]
    for v in basis:
        w = hamming_weight(v)
        if w != 0:
            min_w = min(min_w, w)
    return min_w

def run_size(n_vars, ratio=1.5, k=3, trials=5):
    n_clauses = int(n_vars * ratio)
    weights = []
    for _ in range(trials):
        A = random_k_sat_matrix(n_vars, n_clauses, k)
        w = min_clause_dual_weight(A)
        if w is not None:
            weights.append(w)
    if not weights:
        return None
    avg_w = np.mean(weights)
    return {
        "n_vars": n_vars,
        "n_clauses": n_clauses,
        "avg_dual_weight": avg_w,
        "avg_dual_weight_ratio": avg_w / n_clauses
    }

if __name__ == "__main__":
    sizes = [60, 80, 100, 120, 150]
    for n in sizes:
        stats = run_size(n)
        print(stats)
