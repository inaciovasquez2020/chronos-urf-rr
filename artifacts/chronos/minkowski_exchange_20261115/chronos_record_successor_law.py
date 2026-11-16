#!/usr/bin/env python3
"""Exact finite enumeration for the record-minimum successor-count law.
No external dependencies. Permutation indices are 1-based in the mathematical text.
"""
import itertools
import math
from fractions import Fraction


def law(n, i):
    """P[K=k | v_i is record low], exact rational beta-binomial(i,1)."""
    N = n - i
    return [Fraction(math.comb(N, k) * i * math.factorial(k + i - 1) * math.factorial(N - k),
                     math.factorial(N + i)) for k in range(N + 1)]


def exhaust(n, i):
    N = n - i
    hist = [0] * (N + 1)
    for perm in itertools.permutations(range(n)):
        v = perm[i - 1]
        if v == min(perm[:i]):
            hist[sum(w > v for w in perm[i:])] += 1
    denominator = sum(hist)
    return [Fraction(x, denominator) for x in hist], denominator


def main():
    tested = 0
    for n in range(2, 9):
        for i in range(1, n + 1):
            actual, total = exhaust(n, i)
            expected = law(n, i)
            assert actual == expected, (n, i, actual, expected)
            assert total == math.factorial(n) // i
            assert sum(expected) == 1
            mean = sum(k * pk for k, pk in enumerate(expected))
            assert mean == Fraction((n - i) * i, i + 1)
            tested += 1
        print(f'n={n}: all {n} record positions PASS')
    print('STATUS := COMPUTATION_PASS')
    print(f'POSITION_CASES := {tested}')
    print('ASYMPTOTIC_COLLISION_DECAY := OPEN')


if __name__ == '__main__':
    main()