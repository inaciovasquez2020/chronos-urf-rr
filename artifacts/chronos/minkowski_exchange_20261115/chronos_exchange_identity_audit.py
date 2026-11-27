#!/usr/bin/env python3
"""Exhaustive exact-rational exchange identity audit for 2D permutation posets.
No asymptotic claims. Python standard library only.
"""
from itertools import permutations
from fractions import Fraction


def linear_extensions(pred):
    n = len(pred)
    out = []
    def rec(mask, order):
        if mask == (1 << n)-1:
            out.append(tuple(order))
            return
        for i in range(n):
            if not ((mask >> i) & 1) and (pred[i] & ~mask) == 0:
                rec(mask | (1 << i), order + [i])
    rec(0, [])
    return out


def audit(n):
    count = 0
    for pi in permutations(range(n)):
        pred = [sum(1 << i for i in range(j) if pi[i] < pi[j]) for j in range(n)]
        ext = linear_extensions(pred)
        mins = [i for i, p in enumerate(pred) if p == 0]
        first = {a: [t for t in ext if t[0] == a] for a in mins}
        upsets = {a: {z for z in range(n) if pred[z] & (1 << a)} for a in mins}
        for a in mins:
            for y in mins:
                if a == y:
                    continue
                A, Y = first[a], first[y]
                diff_a = upsets[a] - upsets[y]
                diff_y = upsets[y] - upsets[a]
                allowed_a = [t[1:] for t in A if all(t.index(y) < t.index(z) for z in diff_a)]
                allowed_y = [t[1:] for t in Y if all(t.index(a) < t.index(z) for z in diff_y)]
                mapped = {tuple(a if z == y else z for z in t) for t in allowed_a}
                assert mapped == set(allowed_y), (pi, a, y, 'bijection failed')
                alpha = Fraction(len(allowed_a), len(A))
                beta = Fraction(len(allowed_y), len(Y))
                assert alpha > 0 and beta > 0
                assert Fraction(len(A), len(Y)) == beta / alpha, (pi, a, y)
                count += 1
    return count

if __name__ == '__main__':
    for n in range(2, 7):
        pairs = audit(n)
        print(f'n={n} permutations={__import__("math").factorial(n)} ordered_minimal_pairs={pairs} STATUS=PASS', flush=True)
    print('FINITE_EXCHANGE_IDENTITY=PASS')
    print('ASYMPTOTIC_COLLISION_DECAY=OPEN')