"""Bounded exact graph fixtures from the 2026-11-09 URF manuscript archive.

These checks test finite instances of two analytically described counterexample
families; they do not formally prove the arbitrary-size statements. They never
promote a research claim or execute untrusted source material.

Source archive SHA256:
 f00830e566db256316e8eb2132f238882339c884d33504a8dd94696b7623a50e
Source papers:
 Axioms/The_Xystem_Axiom__Global_Symmetry_and_Local_Spectral_Rigidity.pdf
 Rigidity/Explicit_Local_Cycle_Overlap_Rigidity_for_FO2_in_Bounded_Degree_Graphs.pdf
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations

MAX_EXACT_CYCLE_ORDER = 20
MAX_PRISM_ORDER = 64


def cycle_laplacian_trace_exact(n: int) -> Fraction:
    """Compute tr(L(C_n)^+) over Q, independent of the closed-form formula."""
    if type(n) is not int or not (4 <= n <= MAX_EXACT_CYCLE_ORDER):
        raise ValueError("cycle order outside bounded exact-arithmetic regime")
    mat = [[Fraction(2 if i == j else 0) + Fraction(1, n)
            for j in range(n)] for i in range(n)]
    for i in range(n):
        mat[i][(i + 1) % n] -= 1
        mat[i][(i - 1) % n] -= 1
    rows = [row + [Fraction(i == j) for j in range(n)]
            for i, row in enumerate(mat)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j] != 0), None)
        if pivot is None:
            raise ArithmeticError("connected cycle pseudoinverse construction singular")
        rows[j], rows[pivot] = rows[pivot], rows[j]
        inv_pivot = 1 / rows[j][j]
        rows[j] = [x * inv_pivot for x in rows[j]]
        for i in range(n):
            if i != j:
                factor = rows[i][j]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[j])]
    for i in range(n):
        for j in range(n):
            if sum(mat[i][k] * rows[k][n+j] for k in range(n)) != int(i == j):
                raise ArithmeticError("exact inverse residual failed")
    return sum(rows[i][n+i] for i in range(n)) - 1


def cycle_trace_formula(n: int) -> Fraction:
    if type(n) is not int or n < 4:
        raise ValueError("expected simple cycle order >= 4")
    return Fraction(n * n - 1, 12)


def prism_adjacency(n: int) -> dict[tuple[int,int], set[tuple[int,int]]]:
    """Adjacency of C_n Cartesian-product K_2; simple, connected and cubic."""
    if type(n) is not int or not (4 <= n <= MAX_PRISM_ORDER):
        raise ValueError("prism order outside bounded fixture regime")
    g = {(i, side): {((i-1) % n, side), ((i+1) % n, side), (i, 1-side)}
         for i in range(n) for side in (0, 1)}
    if any(len(adj) != 3 or any(v not in g[w] for w in adj)
           for v, adj in g.items()):
        raise ArithmeticError("not a simple undirected cubic graph")
    return g


def prism_shared_edge_cycle_count(n: int) -> int:
    """Explicit n-1 distinct cycles all containing the same top edge."""
    g = prism_adjacency(n)
    fixed_edge = frozenset({(0,0), (1,0)})
    witnesses: list[frozenset[frozenset[tuple[int,int]]]] = []
    for k in range(1, n):
        walk = [(i,0) for i in range(k+1)] + [(i,1) for i in range(k,-1,-1)]
        if len(walk) != len(set(walk)):
            raise ArithmeticError("cycle not simple")
        edges = frozenset(frozenset({walk[i], walk[(i+1) % len(walk)]})
                          for i in range(len(walk)))
        if fixed_edge not in edges or edges in witnesses:
            raise ArithmeticError("cycle witnesses not distinct or shared-edge")
        if any(len(e) != 2 or any(w not in g[v] for v in e for w in e if v != w)
               for e in edges):
            raise ArithmeticError("witness contains nonedge")
        witnesses.append(edges)
    if any(fixed_edge not in left & right for left,right in combinations(witnesses,2)):
        raise ArithmeticError("overlap witness defective")
    return len(witnesses)


def prism_explicit_vertex_transitive(n: int) -> bool:
    """Check n rotations times two layer-swaps are graph automorphisms."""
    g = prism_adjacency(n)
    vertices = set(g)
    for shift in range(n):
        for swap in (0,1):
            move = lambda v: ((v[0]+shift) % n, v[1] ^ swap)
            if {move(v) for v in vertices} != vertices:
                return False
            if any({move(w) for w in g[v]} != g[move(v)] for v in vertices):
                return False
    return True
