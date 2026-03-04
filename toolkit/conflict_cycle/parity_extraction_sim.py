import random
import networkx as nx
import numpy as np


class GF2Basis:
    """
    Incremental GF(2) row-space basis for fixed dimension dim.
    Stores pivoted basis vectors by their leftmost 1-bit position.
    Complexity per add: O(dim^2) worst-case (dense), but avoids O(t * dim^3) full recomputes.
    """
    def __init__(self, dim: int):
        self.dim = dim
        self.basis = [None] * dim  # basis[i] has pivot at i
        self.rank = 0

    def add(self, v: np.ndarray) -> bool:
        v = (v.copy() & 1).astype(np.uint8)
        for i in range(self.dim):
            if v[i] == 0:
                continue
            b = self.basis[i]
            if b is None:
                self.basis[i] = v
                self.rank += 1
                return True
            v ^= b
        return False


def random_regular_connected(n: int, d: int, seed: int | None = None) -> nx.Graph:
    rng = random.Random(seed)
    while True:
        G = nx.random_regular_graph(d, n, seed=rng.randrange(1 << 30))
        if nx.is_connected(G):
            return G


def edge_list_and_index(G: nx.Graph):
    edges = list(G.edges())
    idx = {}
    for i, (u, v) in enumerate(edges):
        if u > v:
            u, v = v, u
        idx[(u, v)] = i
    return edges, idx


def random_clause(m_vars: int, max_width: int = 6):
    size = random.randint(1, max_width)
    vars_ = random.sample(range(m_vars), size)
    clause = []
    for v in vars_:
        lit = v + 1
        if random.random() < 0.5:
            lit = -lit
        clause.append(lit)
    # dedup + stable order
    clause = tuple(sorted(set(clause), key=lambda x: (abs(x), x)))
    return clause


def clause_vector(clause: tuple[int, ...], m_vars: int) -> np.ndarray:
    v = np.zeros(m_vars, dtype=np.uint8)
    for lit in clause:
        v[abs(lit) - 1] ^= 1
    return v


def resolve(c1: tuple[int, ...], c2: tuple[int, ...], pivot_var: int):
    # pivot_var is 1..m
    s1 = set(c1)
    s2 = set(c2)
    if pivot_var in s1 and -pivot_var in s2:
        out = (s1 | s2) - {pivot_var, -pivot_var}
    elif -pivot_var in s1 and pivot_var in s2:
        out = (s1 | s2) - {pivot_var, -pivot_var}
    else:
        return None
    # tautology check
    if any(-lit in out for lit in out):
        return None
    return tuple(sorted(out, key=lambda x: (abs(x), x)))


def simulate(
    n: int = 80,
    d: int = 3,
    steps: int = 20000,
    seed: int = 0,
    init_clauses: int = 80,
    partner_samples: int = 1,
    max_width: int = 6,
    report_every: int = 2000,
):
    random.seed(seed)

    G = random_regular_connected(n, d, seed=seed)
    edges, _ = edge_list_and_index(G)
    m = len(edges)

    clauses: set[tuple[int, ...]] = set()
    basis = GF2Basis(m)

    for _ in range(init_clauses):
        c = random_clause(m, max_width=max_width)
        clauses.add(c)
        basis.add(clause_vector(c, m))

    max_rank = basis.rank

    clause_list = list(clauses)

    for t in range(1, steps + 1):

        if len(clause_list) < 2:
            break

        c1, c2 = random.sample(clause_list, 2)

        vars1 = {abs(x) for x in c1}
        vars2 = {abs(x) for x in c2}
        common = list(vars1 & vars2)
        if not common:
            continue

        for _ in range(partner_samples):
            pivot = random.choice(common)
            r = resolve(c1, c2, pivot)
            if r is None:
                continue
            if r in clauses:
                continue

            clauses.add(r)
            clause_list.append(r)

            basis.add(clause_vector(r, m))
            if basis.rank > max_rank:
                max_rank = basis.rank

        if report_every and (t % report_every == 0):
            print("t", t, "clauses", len(clauses), "rank", basis.rank, "max_rank", max_rank)

            if max_rank >= m:
                break

    print("nodes", n)
    print("edges", m)
    print("clauses_final", len(clauses))
    print("max_parity_rank", max_rank)
    return {
        "n": n,
        "m": m,
        "clauses": len(clauses),
        "max_rank": max_rank,
    }


if __name__ == "__main__":
    simulate()
