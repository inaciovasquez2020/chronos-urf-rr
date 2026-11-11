#!/usr/bin/env python3
"""Bounded, dependency-free tests for the 4D causal-prefix selection envelope.

Status: finite combinatorics and analytic Chernoff bound. Does not prove
uniform-linear-extension Minkowski sampling convergence.
"""
from fractions import Fraction
from functools import lru_cache
from math import comb, exp, log, sqrt


def transitive_poset(n, edge_bits):
    pred = [0] * n
    j = 0
    for v in range(n):
        for u in range(v):
            if (edge_bits >> j) & 1:
                pred[v] |= 1 << u
            j += 1
    for v in range(n):
        for u in range(v):
            if (pred[v] >> u) & 1:
                pred[v] |= pred[u]
    return tuple(pred)


def prefix_inclusion_probabilities(pred, n):
    N = len(pred)
    full = (1 << N) - 1
    @lru_cache(None)
    def extensions(mask):
        if mask == full:
            return 1
        return sum(extensions(mask | (1 << v)) for v in range(N)
                   if not (mask >> v) & 1 and not pred[v] & ~mask)
    # Count prefixes using integer DP over order ideals.
    cur = {0: 1}
    for _ in range(n):
        nxt = {}
        for mask, ways in cur.items():
            for v in range(N):
                if not (mask >> v) & 1 and not pred[v] & ~mask:
                    m = mask | (1 << v)
                    nxt[m] = nxt.get(m, 0) + ways
        cur = nxt
    den = extensions(0)
    assert sum(ways * extensions(m) for m, ways in cur.items()) == den
    return tuple(Fraction(sum(ways * extensions(mask) for mask, ways in cur.items()
                              if (mask >> v) & 1), den) for v in range(N))


def exact_small_poset_test():
    checks = 0
    for N in range(2, 6):
        for edges in range(1 << comb(N, 2)):
            P = transitive_poset(N, edges)
            for n in range(1, N+1):
                q = prefix_inclusion_probabilities(P, n)
                assert sum(q) == n
                for v in range(N):
                    if P[v].bit_count() >= n:
                        assert q[v] == 0
                    for u in range(N):
                        if (P[v] >> u) & 1:
                            assert q[u] >= q[v]
                checks += 1
    return checks


def volume_fraction_cdf(s):
    if s <= 0: return 0.0
    if s >= 1: return 1.0
    return 6 * sqrt(s) - 3*s + 3*s*log(s) - 2*s**1.5


def boundary_certificate(N, n, C=8):
    # Pr(s(z) > delta for at least one event in any n-prefix)
    # <= N exp[-(C-1)^2/(2C) (n+ln N)], if delta<1.
    assert N >= n >= 1 and C > 1
    delta = C * (n + log(N)) / (N-1)
    if delta >= 1:
        return {'N':N,'n':n,'delta':delta,'applicable':False}
    exponent = (C-1)**2 / (2*C)
    upper = N * exp(-exponent * (n+log(N)))
    shell_fraction = volume_fraction_cdf(delta)
    return {'N':N,'n':n,'delta':delta,'failure_upper':upper,
            'expected_shell_fraction':shell_fraction,
            'expected_shell_size':N*shell_fraction, 'applicable':True}


def main():
    checks = exact_small_poset_test()
    assert checks == sum((N*(1<<comb(N,2)) for N in range(2,6)))
    print('FINITE_POSET_TESTS :=',checks)
    print('EXACT_PREFIX_ANCESTOR_EXCLUSION := PASS')
    for N,n in ((1000,2),(10000,10),(100000,100),(1000000,1000)):
        print('BOUNDARY_CERTIFICATE :=', boundary_certificate(N,n))
    print('GROWING_PREFIX_BOUND := PROVED_BY_BINOMIAL_CHERNOFF')
    print('UNIFORM_EXTENSION_SELECTION_INSIDE_SHELL := OPEN')
    print('MINKOWSKI_PROFILE_LIMIT := OPEN')


if __name__ == '__main__':
    main()
