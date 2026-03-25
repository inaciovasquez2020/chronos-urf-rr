from models.patch_rank_expansion.patch_rank_expansion import (
    random_k_sat_matrix,
    patch_rank_density,
)
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

def run_trial(n_vars=80, n_clauses=120, k=3, R=2):
    A = random_k_sat_matrix(n_vars, n_clauses, k)
    densities = patch_rank_density(A, R)
    min_patch_density = min(densities)
    dual_w = min_clause_dual_weight(A)
    return {
        "min_patch_density": min_patch_density,
        "clause_dual_min_weight": dual_w,
    }

if __name__ == "__main__":
    trials = 10
    results = []
    for _ in range(trials):
        stats = run_trial()
        print(stats)
        results.append(stats)

    avg_patch = np.mean([r["min_patch_density"] for r in results])
    dual_vals = [r["clause_dual_min_weight"] for r in results if r["clause_dual_min_weight"] is not None]
    avg_dual = np.mean(dual_vals) if dual_vals else None

    print("\nAverage patch density:", avg_patch)
    print("Average clause-dual min weight:", avg_dual)
