#!/usr/bin/env python3
import itertools
import math
import os
import random
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set, Optional

# ----------------------------
# Utilities
# ----------------------------

def bits_to_int(bits):
    x = 0
    for i,b in enumerate(bits):
        x |= (b & 1) << i
    return x

def int_to_bits(x, n):
    return [(x >> i) & 1 for i in range(n)]

def log2_ceil(x: int) -> int:
    if x <= 1:
        return 0
    return math.ceil(math.log2(x))

# ----------------------------
# CNF model (variables indexed 0..m-1)
# clause is list of literals; literal is (var, sign) where sign=1 means x, sign=0 means ¬x
# ----------------------------

Lit = Tuple[int, int]
Clause = List[Lit]
CNF = List[Clause]

def eval_lit(a_bits: List[int], lit: Lit) -> int:
    v, sign = lit
    x = a_bits[v]
    return x if sign == 1 else (1 - x)

def eval_clause(a_bits: List[int], clause: Clause) -> int:
    return 1 if any(eval_lit(a_bits, lit) == 1 for lit in clause) else 0

def violated_clauses(a_bits: List[int], cnf: CNF) -> List[int]:
    return [i for i,C in enumerate(cnf) if eval_clause(a_bits, C) == 0]

def canonical_search_output(a_bits: List[int], cnf: CNF) -> int:
    v = violated_clauses(a_bits, cnf)
    if not v:
        return -1
    return v[0]

# ----------------------------
# Tseitin on graph G=(V,E), variables are edges, constraints per vertex are XOR over incident edges = f(v)
# encoded as CNF via all falsifying assignments (standard parity CNF)
# ----------------------------

@dataclass
class Graph:
    n: int
    edges: List[Tuple[int,int]]  # undirected, vertices 0..n-1

def cycle_graph(n: int) -> Graph:
    edges = [(i, (i+1) % n) for i in range(n)]
    return Graph(n=n, edges=edges)

def random_d_regular(n: int, d: int, seed: int) -> Graph:
    rng = random.Random(seed)
    stubs = []
    for v in range(n):
        stubs.extend([v]*d)
    rng.shuffle(stubs)
    edges = []
    tries = 0
    while stubs:
        tries += 1
        if tries > 200000:
            raise RuntimeError("failed to generate d-regular multigraph quickly")
        a = stubs.pop()
        b = stubs.pop()
        if a == b:
            stubs.extend([a,b])
            rng.shuffle(stubs)
            continue
        e = (a,b) if a < b else (b,a)
        edges.append(e)
    edges = list(dict.fromkeys(edges))
    return Graph(n=n, edges=edges)

def build_tseitin_cnf(G: Graph, f_bits: List[int]) -> Tuple[CNF, int]:
    # variables = edges, index by position
    m = len(G.edges)
    inc = [[] for _ in range(G.n)]
    for ei,(u,v) in enumerate(G.edges):
        inc[u].append(ei)
        inc[v].append(ei)

    cnf: CNF = []
    for v in range(G.n):
        vars_v = inc[v]
        d = len(vars_v)
        # parity equation: xor(vars_v) = f(v)
        # CNF encoding: forbid assignments with xor != f(v)
        # for each bad assignment b in {0,1}^d with xor(b) != f(v), add clause that excludes it:
        # clause is OR over literals (x_i if b_i=0 else ¬x_i)
        for b in itertools.product([0,1], repeat=d):
            x = 0
            for bit in b:
                x ^= bit
            if x == f_bits[v]:
                continue
            clause: Clause = []
            for idx,bit in enumerate(b):
                var = vars_v[idx]
                # exclude assignment bit: literal true when variable differs from bit
                # if bit=0 -> include x; if bit=1 -> include ¬x
                clause.append((var, 1 if bit == 0 else 0))
            cnf.append(clause)
    return cnf, m

# ----------------------------
# XOR-SAT random: choose r linear equations over m vars; encode each equation as parity CNF over its support (small width)
# ----------------------------

def build_random_xorsat_cnf(m: int, r: int, width: int, seed: int) -> CNF:
    rng = random.Random(seed)
    cnf: CNF = []
    for _ in range(r):
        S = rng.sample(range(m), width)
        rhs = rng.randrange(2)
        # parity CNF on vars S: xor(S) = rhs
        for b in itertools.product([0,1], repeat=width):
            x = 0
            for bit in b:
                x ^= bit
            if x == rhs:
                continue
            clause: Clause = []
            for j,bit in enumerate(b):
                var = S[j]
                clause.append((var, 1 if bit == 0 else 0))
            cnf.append(clause)
    return cnf

# ----------------------------
# Random k-CNF: generate until unsat (small m) by brute check
# ----------------------------

def is_sat_bruteforce(cnf: CNF, m: int) -> bool:
    for a in range(1<<m):
        bits = int_to_bits(a, m)
        if all(eval_clause(bits, C) == 1 for C in cnf):
            return True
    return False

def build_random_kcnf_unsat(m: int, k: int, clauses: int, seed: int, max_tries: int = 2000) -> CNF:
    rng = random.Random(seed)
    for t in range(max_tries):
        cnf: CNF = []
        for _ in range(clauses):
            vs = rng.sample(range(m), k)
            clause = []
            for v in vs:
                sign = rng.randrange(2)  # 1 positive, 0 negative
                clause.append((v, sign))
            cnf.append(clause)
        if not is_sat_bruteforce(cnf, m):
            return cnf
    raise RuntimeError("failed to find unsat random k-CNF in max_tries")

# ----------------------------
# PHP(m+1 -> m) encoded as CNF:
# vars x_{i,j}: pigeon i goes to hole j
# constraints:
#  (1) each pigeon in some hole: OR_j x_{i,j}
#  (2) no pigeon in two holes: ¬x_{i,j} ∨ ¬x_{i,j'}
#  (3) no two pigeons same hole: ¬x_{i,j} ∨ ¬x_{i',j}
# Small sizes only.
# ----------------------------

def build_php_cnf(pigeons: int, holes: int) -> Tuple[CNF, int]:
    # var index: i*holes + j
    m = pigeons * holes
    cnf: CNF = []
    # (1)
    for i in range(pigeons):
        cnf.append([(i*holes + j, 1) for j in range(holes)])
    # (2)
    for i in range(pigeons):
        for j in range(holes):
            for jp in range(j+1, holes):
                cnf.append([(i*holes + j, 0), (i*holes + jp, 0)])
    # (3)
    for j in range(holes):
        for i in range(pigeons):
            for ip in range(i+1, pigeons):
                cnf.append([(i*holes + j, 0), (ip*holes + j, 0)])
    return cnf, m

# ----------------------------
# Communication lower bound proxy for Search_F:
# Build function f(x,y) by choosing canonical violated clause index.
# Compute fooling set lower bound on deterministic CC:
#   size(FS) <= 2^{CC}
# so CC >= log2 |FS|.
# For small sizes we compute a maximal fooling set by exact backtracking.
# ----------------------------

def split_assignment(a_bits: List[int], X: List[int], Y: List[int]) -> Tuple[int,int]:
    x = 0
    y = 0
    for i,v in enumerate(X):
        x |= (a_bits[v] & 1) << i
    for i,v in enumerate(Y):
        y |= (a_bits[v] & 1) << i
    return x,y

def build_search_function_table(cnf: CNF, m: int, X: List[int], Y: List[int]) -> Dict[Tuple[int,int], int]:
    table: Dict[Tuple[int,int], int] = {}
    for a in range(1<<m):
        bits = int_to_bits(a, m)
        out = canonical_search_output(bits, cnf)
        if out < 0:
            continue
        x,y = split_assignment(bits, X, Y)
        table[(x,y)] = out
    return table

def fooling_set_greedy(table, nx, ny):
    items = [(x,y,o) for ((x,y),o) in table.items()]
    items.sort(key=lambda t: (t[2], t[0], t[1]))
    S = []
    for (x,y,o) in items:
        good = True
        for (x1,y1,o1) in S:
            if o1 == o:
                good = False
                break
            if table.get((x1,y), None) == o1 and table.get((x,y1), None) == o:
                good = False
                break
        if good:
            S.append((x,y,o))
    return len(S)

# ----------------------------
# Suite runner
# ----------------------------

@dataclass
class Case:
    name: str
    cnf: CNF
    m: int
    X: List[int]
    Y: List[int]

def balanced_split(m: int, seed: int) -> Tuple[List[int], List[int]]:
    rng = random.Random(seed)
    vars_ = list(range(m))
    rng.shuffle(vars_)
    mid = m//2
    X = vars_[:mid]
    Y = vars_[mid:]
    return X,Y

def run_case(case: Case) -> Dict[str, str]:
    table = build_search_function_table(case.cnf, case.m, case.X, case.Y)
    nx = 1 << len(case.X)
    ny = 1 << len(case.Y)
    # sanity: total
    if len(table) < nx*ny:
        # missing entries are allowed if some assignments satisfy all clauses (should not for unsat), but keep report
        pass
    fs = fooling_set_greedy(table, nx, ny)
    lb_cc = log2_ceil(fs)
    return {
        "case": case.name,
        "m": str(case.m),
        "|X|": str(len(case.X)),
        "|Y|": str(len(case.Y)),
        "fooling_set_size": str(fs),
        "CC_lower_bound_bits": str(lb_cc),
    }

def main():
    random.seed(0)

    cases: List[Case] = []

    # Tseitin: cycle vs random regular (tiny n)
    # cycle graph (easy-ish) n=8
    Gc = cycle_graph(8)
    fc = [0]*Gc.n
    fc[0] = 1
    cnf_c, m_c = build_tseitin_cnf(Gc, fc)
    Xc,Yc = balanced_split(m_c, seed=1)
    cases.append(Case(name="tseitin_cycle_n8", cnf=cnf_c, m=m_c, X=Xc, Y=Yc))

    # "expander-ish" random 3-regular multigraph n=10
    Gr = random_d_regular(10, 3, seed=2)
    fr = [0]*Gr.n
    fr[0] = 1
    cnf_r, m_r = build_tseitin_cnf(Gr, fr)
    Xr,Yr = balanced_split(m_r, seed=3)
    cases.append(Case(name="tseitin_rand3_n10", cnf=cnf_r, m=m_r, X=Xr, Y=Yr))

    # XOR-SAT unsat-ish small: choose enough equations
    m = 12
    xcnf = build_random_xorsat_cnf(m=m, r=9, width=4, seed=4)
    if is_sat_bruteforce(xcnf, m):
        # force unsat by adding one contradictory width-1 clause pair x0 and ¬x0
        xcnf.append([(0,1)])
        xcnf.append([(0,0)])
    Xx,Yx = balanced_split(m, seed=5)
    cases.append(Case(name="xorsat_m12_r9_w4", cnf=xcnf, m=m, X=Xx, Y=Yx))

    # PHP: pigeons=4, holes=3 (unsat)
    php, m_php = build_php_cnf(pigeons=4, holes=3)
    Xp,Yp = balanced_split(m_php, seed=6)
    cases.append(Case(name="php_4_to_3", cnf=php, m=m_php, X=Xp, Y=Yp))

    # random k-CNF unsat small
    m_k = 14
    kcnf = build_random_kcnf_unsat(m=m_k, k=3, clauses=60, seed=7)
    Xk,Yk = balanced_split(m_k, seed=8)
    cases.append(Case(name="rand3cnf_m14_c60_unsat", cnf=kcnf, m=m_k, X=Xk, Y=Yk))

    rows = []
    for c in cases:
        rows.append(run_case(c))

    # print markdown-ish
    headers = ["case","m","|X|","|Y|","fooling_set_size","CC_lower_bound_bits"]
    print("\t".join(headers))
    for r in rows:
        print("\t".join(r[h] for h in headers))

if __name__ == "__main__":
    main()
