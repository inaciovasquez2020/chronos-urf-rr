from models.patch_rank_expansion.patch_rank_expansion import random_k_sat_matrix
from models.patch_rank_expansion.dual_tools import gf2_nullspace_basis, hamming_weight
from collections import deque
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

def bipartite_girth(A):
    n_clauses, n_vars = A.shape
    N = n_clauses + n_vars

    adj = [[] for _ in range(N)]

    for i in range(n_clauses):
        for v in np.where(A[i] == 1)[0]:
            adj[i].append(n_clauses + v)
            adj[n_clauses + v].append(i)

    min_cycle = float("inf")

    for start in range(N):
        dist = [-1]*N
        parent = [-1]*N
        q = deque([start])
        dist[start] = 0

        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    q.append(v)
                elif parent[u] != v:
                    cycle_len = dist[u] + dist[v] + 1
                    if cycle_len % 2 == 0:
                        min_cycle = min(min_cycle, cycle_len)

    if min_cycle == float("inf"):
        return None
    return min_cycle

def run_trial(n_vars=80, n_clauses=120, k=3):
    A = random_k_sat_matrix(n_vars, n_clauses, k)
    g = bipartite_girth(A)
    dual_w = min_clause_dual_weight(A)
    return {
        "bipartite_girth": g,
        "clause_dual_min_weight": dual_w,
    }

if __name__ == "__main__":
    trials = 10
    for _ in range(trials):
        stats = run_trial()
        print(stats)
