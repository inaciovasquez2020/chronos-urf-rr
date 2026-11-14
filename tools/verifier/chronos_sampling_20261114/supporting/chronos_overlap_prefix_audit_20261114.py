#!/usr/bin/env python3
"""Finite-poset audit for an overlapping-future observable; stdlib only.
Does not evaluate the continuous Minkowski overlap integral or prove an infinite limit.
"""
from itertools import combinations, permutations, product
from fractions import Fraction


def posets(n):
    pairs=list(combinations(range(n),2))
    for states in product(range(3),repeat=len(pairs)):
        edges=set()
        for (a,b),v in zip(pairs,states):
            if v==1:edges.add((a,b))
            if v==2:edges.add((b,a))
        if all((a,c) in edges for a,b in edges for bb,c in edges if bb==b):
            yield frozenset(edges)

def p2(edges):
    le=[p for p in permutations(range(4)) if all(p.index(a)<p.index(b) for a,b in edges)]
    return Fraction(sum((p[0],p[1]) in edges for p in le),len(le))

def two_incomparable_sources_with_two_common_futures(edges):
    n=4
    return int(any(
        (x,y) not in edges and (y,x) not in edges and
        all((x,z) in edges and (y,z) in edges for z in range(n) if z not in (x,y))
        for x,y in combinations(range(n),2)
    ))

P=list(posets(4))
assert len(P)==219
C=[e for e in P if two_incomparable_sources_with_two_common_futures(e)]
assert all(len(e) in (4,5) for e in C)
assert all(p2(e)==0 for e in C)
assert len(C)>0
# Geometric moment from the previously audited exact null-coordinate integral.
assert Fraction(12,35280)==Fraction(1,2940)
print('LABELED_POSETS :=',len(P))
print('OVERLAP_EVENT_LABELED_POSETS :=',len(C))
print('OVERLAP_EVENT_P2_ZERO := PASS')
print('GEOMETRIC_DECOMPOSITION := B = 6*(E[J_plus(X,Y)^2] - 2/35280)')
print('MINKOWSKI_OVERLAP_SECOND_MOMENT := OPEN')
print('FIXED_PREFIX_LIMIT_UNIQUENESS := OPEN')
print('LEAN := NOT_RUN')
print('STATUS := COMPUTATION_PASS_FINITE_ONLY')
