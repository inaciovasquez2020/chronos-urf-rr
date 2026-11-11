#!/usr/bin/env python3
"""Exact ideal-prefix ancestor-marginal identity; independent enumerative check.
Python standard library. All rational calculations exact. N<=5, bounded.
"""
from fractions import Fraction
from itertools import combinations
from math import comb


def transitive_closure(n, bits):
    predecessors = [0] * n
    b = 0
    for j in range(n):
        for i in range(j):
            if (bits >> b) & 1:
                predecessors[j] |= 1 << i
            b += 1
    for j in range(n):
        for i in range(j):
            if (predecessors[j] >> i) & 1:
                predecessors[j] |= predecessors[i]
    return predecessors


def linear_extensions(pred):
    n = len(pred)
    def rec(mask, prefix):
        if mask == (1 << n)-1:
            yield prefix
            return
        for v in range(n):
            if not (mask >> v) & 1 and not (pred[v] & ~mask):
                yield from rec(mask | (1 << v), prefix + (v,))
    yield from rec(0, ())


def verify(pred, n):
    N = len(pred)
    ext = list(linear_extensions(pred))
    assert ext
    denominator = len(ext)
    count = [0] * N
    relation_count = 0
    for order in ext:
        prefix = set(order[:n])
        for x in prefix:
            count[x] += 1
        relation_count += sum(((pred[y] >> x) & 1) for x, y in combinations(sorted(prefix), 2))
        # The sorted-by-original-label enumeration is valid because the poset
        # only uses lower-to-higher label relations.
    q = [Fraction(c, denominator) for c in count]
    assert sum(q) == n
    predicted = sum(pred[y].bit_count() * q[y] for y in range(N))
    observed = Fraction(relation_count, denominator)
    assert predicted == observed
    for y in range(N):
        if pred[y].bit_count() >= n:
            assert q[y] == 0
        for x in range(y):
            if (pred[y] >> x) & 1:
                assert q[x] >= q[y]
    expected_p = predicted / comb(n, 2)
    direct_p = observed / comb(n, 2)
    assert expected_p == direct_p
    uniform_target = Fraction(sum(p.bit_count() for p in pred), comb(N, 2))
    # Conditional finite-P bias (not the Minkowski average):
    centered = sum(pred[y].bit_count() * (q[y] - Fraction(comb(n,2),comb(N,2)))
                   for y in range(N)) / comb(n,2)
    assert expected_p - uniform_target == centered
    return expected_p, centered


def main():
    count = 0
    maxabs = Fraction(0)
    witnessed = None
    for N in range(2, 6):
        for bits in range(1 << comb(N, 2)):
            pred = transitive_closure(N, bits)
            for n in range(2, N+1):
                _, bias = verify(pred, n)
                if n < N and abs(bias) > maxabs:
                    maxabs = abs(bias)
                    witnessed = (N, bits, n, str(bias))
                count += 1
    print('EXHAUSTIVE_N_UP_TO := 5')
    print('EXACT_TEST_CASES :=', count)
    print('MARGINAL_ANCESTOR_PAIR_IDENTITY := PASS')
    print('SHALLOW_PAST_EXCLUSION := PASS')
    print('FINITE_POSET_BIAS_IDENTITY := PASS')
    print('MAX_ABSOLUTE_TESTED_BIAS :=', maxabs)
    print('WITNESS :=', witnessed)
    print('MINKOWSKI_ASYMPTOTIC_BIAS := OPEN')


if __name__ == '__main__':
    main()
