import random
from collections import deque
import numpy as np

def random_k_sat_matrix(n_vars, n_clauses, k):
    A = np.zeros((n_clauses, n_vars), dtype=np.uint8)
    for i in range(n_clauses):
        vars_ = random.sample(range(n_vars), k)
        for v in vars_:
            A[i, v] = 1
    return A

def gf2_rank(M):
    M = M.copy()
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if M[i, c]:
                pivot = i
                break
        if pivot is None:
            continue
        M[[r, pivot]] = M[[pivot, r]]
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        r += 1
        if r == rows:
            break
    return r

def clause_graph(A):
    n_clauses, n_vars = A.shape
    adj = [[] for _ in range(n_clauses)]
    var_to_clauses = [[] for _ in range(n_vars)]
    for i in range(n_clauses):
        for v in np.where(A[i] == 1)[0]:
            var_to_clauses[v].append(i)
    for clauses in var_to_clauses:
        for i in clauses:
            for j in clauses:
                if i != j:
                    adj[i].append(j)
    return adj

def radius_patch(adj, start, R):
    visited = {start}
    q = deque([(start, 0)])
    while q:
        node, dist = q.popleft()
        if dist == R:
            continue
        for nei in adj[node]:
            if nei not in visited:
                visited.add(nei)
                q.append((nei, dist + 1))
    return sorted(visited)

def patch_rank_density(A, R):
    adj = clause_graph(A)
    densities = []
    for start in range(len(adj)):
        patch = radius_patch(adj, start, R)
        subA = A[patch]
        rank = gf2_rank(subA)
        density = rank / max(1, subA.shape[0])
        densities.append(density)
    return densities

def run_experiment(n_vars=200, n_clauses=300, k=3, R=2):
    A = random_k_sat_matrix(n_vars, n_clauses, k)
    densities = patch_rank_density(A, R)
    return {
        "min_density": min(densities),
        "avg_density": sum(densities) / len(densities),
        "max_density": max(densities)
    }

if __name__ == "__main__":
    print(run_experiment())
