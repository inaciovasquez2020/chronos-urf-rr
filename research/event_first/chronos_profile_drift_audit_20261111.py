#!/usr/bin/env python3
"""Exact birth-profile drift identity and finite causal-poset regression.
No dependencies or repo writes. Bounded exhaustive forward-edge closures N<=5.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations
from math import comb

def poset(n, edges):
    past = [0] * n
    bit = 0
    for j in range(n):
        for i in range(j):
            if (edges >> bit) & 1:
                past[j] |= 1 << i
            bit += 1
    for j in range(n):
        for i in range(j):
            if (past[j] >> i) & 1:
                past[j] |= past[i]
    return past

def extensions(past):
    n = len(past)
    def walk(seq, seen):
        if len(seq) == n:
            yield seq
        else:
            for v in range(n):
                if not (seen >> v) & 1 and (past[v] & ~seen) == 0:
                    yield from walk(seq + (v,), seen | (1 << v))
    yield from walk((), 0)

def type_key(past, vertices):
    """Unlabeled induced poset signature, both directions."""
    return min(tuple(int(bool((past[p[j]] >> p[i]) & 1))
                     for i in range(len(p)) for j in range(len(p)) if i != j)
               for p in permutations(vertices))

def frequencies(past, vertices, k, forced=None):
    vertices = tuple(vertices)
    options = (tuple(s for s in combinations(vertices, k) if forced in s)
               if forced is not None else tuple(combinations(vertices, k)))
    if not options:
        return {}
    weights = Counter(type_key(past, s) for s in options)
    return {t: F(c, len(options)) for t, c in weights.items()}

def difference(a, b):
    return {x: a.get(x, F(0)) - b.get(x, F(0)) for x in a.keys() | b.keys()}

def scale_add(a, ca, b, cb):
    return {x: ca*a.get(x, F(0)) + cb*b.get(x, F(0))
            for x in a.keys() | b.keys()}

def verify(n, edge_mask):
    past = poset(n, edge_mask)
    exts = list(extensions(past))
    assert exts
    tests = 0
    for k in range(2, min(4, n) + 1):
        avgs = [Counter() for _ in range(n + 1)]
        drift = [Counter() for _ in range(n + 1)]
        for extension in exts:
            prior = None
            for m in range(k, n + 1):
                current = frequencies(past, extension[:m], k)
                for t, val in current.items():
                    avgs[m][t] += val
                if m > k:
                    last = extension[m - 1]
                    appended = frequencies(past, extension[:m], k, forced=last)
                    coeff = F(k, m)
                    rhs = scale_add(prior, 1-coeff, appended, coeff)
                    assert current == rhs, (n, edge_mask, k, m, current, rhs)
                    ds = difference(appended, prior)
                    for t, val in ds.items():
                        drift[m][t] += coeff * val
                    tests += 1
                prior = current
        q = {t: F(v, len(exts)) for t, v in avgs[n].items()}
        for start in range(k, n + 1):
            lhs = difference(q, {t: F(v, len(exts)) for t,v in avgs[start].items()})
            total = Counter()
            for m in range(start + 1, n + 1):
                for t,v in drift[m].items():
                    total[t] += F(v, len(exts))
            assert all(lhs.get(t,0) == total.get(t,0) for t in lhs.keys()|total.keys())
            tests += 1
    return tests

def main():
    total = 0
    for n in range(2, 6):
        for mask in range(1 << comb(n, 2)):
            total += verify(n, mask)
    print('EXACT_PROFILE_DRIFT_TESTS :=',total)
    print('ALL_FINITE_TELESCOPING_IDENTITIES := PASS')
    print('MINKOWSKI_DRIFT_TAIL := OPEN')

if __name__ == '__main__': main()
