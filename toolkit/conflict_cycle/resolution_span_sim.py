import itertools
import random
from collections import deque

import networkx as nx
import numpy as np


# ----------------------------
# GF(2) rank
# ----------------------------

def gf2_rank(rows: list[np.ndarray]) -> int:
    if not rows:
        return 0
    A = np.array(rows, dtype=np.uint8) & 1
    m, n = A.shape
    r = 0
    c = 0
    while r < m and c < n:
        piv = None
        for i in range(r, m):
            if A[i, c]:
                piv = i
                break
        if piv is None:
            c += 1
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i, :] ^= A[r, :]
        r += 1
        c += 1
    return r


# ----------------------------
# Tseitin CNF (XOR at vertices)
# ----------------------------

# Variables are edges of G. Each edge e is assigned an index 0..m-1.
# Tseitin constraint at vertex v: XOR_{e incident to v} x_e = charge[v] (in {0,1})
# CNF encoding: for each falsifying assignment to incident edges, add a clause forbidding it.

def tseitin_cnf(G: nx.Graph, charge: dict[int, int]):
    edges = list(G.edges())
    edge_index = {}
    for idx, (u, v) in enumerate(edges):
        if u > v:
            u, v = v, u
        edge_index[(u, v)] = idx

    clauses = []
    for v in G.nodes():
        inc = []
        for u in G.neighbors(v):
            a, b = (u, v) if u < v else (v, u)
            inc.append(edge_index[(a, b)])

        deg = len(inc)
        rhs = charge[v] & 1

        # enumerate all assignments to incident edges; add clause for those with wrong parity
        for bits in itertools.product([0, 1], repeat=deg):
            if (sum(bits) & 1) == rhs:
                continue
            # forbidding clause: for each variable in assignment,
            # if bit=1 then add ¬x (literal negative), if bit=0 then add x (positive)
            clause = []
            for var, bit in zip(inc, bits):
                lit = -(var + 1) if bit == 1 else (var + 1)
                clause.append(lit)
            clauses.append(tuple(sorted(clause, key=lambda z: (abs(z), z))))
    return edges, clauses


# ----------------------------
# Resolution engine (toy)
# ----------------------------

def is_tautology(clause: tuple[int, ...]) -> bool:
    s = set(clause)
    return any(-lit in s for lit in s)

def resolve(c1: tuple[int, ...], c2: tuple[int, ...], piv: int):
    # piv is a positive variable index (1..m)
    # require piv in one clause and -piv in the other (or vice versa)
    s1 = set(c1)
    s2 = set(c2)
    if piv in s1 and -piv in s2:
        out = (s1 | s2) - {piv, -piv}
    elif -piv in s1 and piv in s2:
        out = (s1 | s2) - {piv, -piv}
    else:
        return None
    out_t = tuple(sorted(out, key=lambda z: (abs(z), z)))
    if is_tautology(out_t):
        return None
    return out_t

def clause_var_vector(clause: tuple[int, ...], m_vars: int) -> np.ndarray:
    # proxy for "cut-span": incidence of variables in the clause, mod 2
    v = np.zeros(m_vars, dtype=np.uint8)
    for lit in clause:
        v[abs(lit) - 1] ^= 1
    return v

def simulate_resolution_span(G: nx.Graph,
                             live_cap: int = 400,
                             max_steps: int = 20000,
                             seed: int = 0):
    random.seed(seed)

    # odd charge => unsat
    charge = {v: 0 for v in G.nodes()}
    charge[random.choice(list(G.nodes()))] = 1

    edges, init_clauses = tseitin_cnf(G, charge)
    m_vars = len(edges)

    # Active "live" multiset of clauses
    live = deque()
    seen = set()
    agenda = deque()

    for c in init_clauses:
        if c not in seen:
            seen.add(c)
            live.append(c)
            agenda.append(c)

    def current_span_rank():
        rows = [clause_var_vector(c, m_vars) for c in live]
        return gf2_rank(rows)

    span_series = []
    max_span = current_span_rank()
    span_series.append(max_span)

    # index clauses by variable occurrence for faster pairing
    pos_index = [set() for _ in range(m_vars + 1)]
    neg_index = [set() for _ in range(m_vars + 1)]

    def index_clause(c):
        for lit in c:
            v = abs(lit)
            if lit > 0:
                pos_index[v].add(c)
            else:
                neg_index[v].add(c)

    for c in list(live):
        index_clause(c)

    steps = 0
    while steps < max_steps:
        steps += 1
        if not agenda:
            # pick a random live clause to keep search moving
            agenda.append(random.choice(list(live)))

        c = agenda.popleft()
        if c == tuple():
            break

        # choose a pivot literal from c
        if not c:
            break
        piv_lit = random.choice(list(c))
        piv = abs(piv_lit)

        # partner clauses must contain opposite literal
        partners = neg_index[piv] if piv_lit > 0 else pos_index[piv]
        if not partners:
            continue

        # sample a few partners
        partner_list = list(partners)
        random.shuffle(partner_list)
        for d in partner_list[: min(8, len(partner_list))]:
            r = resolve(c, d, piv)
            if r is None:
                continue
            if r == tuple():
                live.append(r)
                span_series.append(current_span_rank())
                return {
                    "unsat": True,
                    "steps": steps,
                    "m_vars": m_vars,
                    "n_nodes": G.number_of_nodes(),
                    "m_edges": G.number_of_edges(),
                    "max_span": max(max_span, span_series[-1]),
                    "span_series": span_series,
                }
            if r not in seen:
                seen.add(r)
                live.append(r)
                agenda.append(r)
                index_clause(r)

                # bounded "live" memory (delete oldest)
                while len(live) > live_cap:
                    old = live.popleft()
                    # do not remove from seen; we model deletion not forgetting
                    for lit in old:
                        v = abs(lit)
                        if lit > 0:
                            pos_index[v].discard(old)
                        else:
                            neg_index[v].discard(old)

                rk = current_span_rank()
                span_series.append(rk)
                if rk > max_span:
                    max_span = rk

    return {
        "unsat": False,
        "steps": steps,
        "m_vars": m_vars,
        "n_nodes": G.number_of_nodes(),
        "m_edges": G.number_of_edges(),
        "max_span": max_span,
        "span_series": span_series,
    }


# ----------------------------
# Driver
# ----------------------------

def random_regular_connected(n: int, d: int, seed: int):
    rng = random.Random(seed)
    while True:
        G = nx.random_regular_graph(d, n, seed=rng.randrange(1 << 30))
        if nx.is_connected(G):
            return G

if __name__ == "__main__":
    # small regime for resolution simulation
    n = 40
    d = 3
    live_cap = 350
    max_steps = 25000
    seed = 0

    G = random_regular_connected(n, d, seed)

    out = simulate_resolution_span(G, live_cap=live_cap, max_steps=max_steps, seed=seed)

    print("n_nodes", out["n_nodes"])
    print("m_edges", out["m_edges"])
    print("m_vars", out["m_vars"])
    print("steps", out["steps"])
    print("unsat_found", out["unsat"])
    print("max_live_span_rank", out["max_span"])
