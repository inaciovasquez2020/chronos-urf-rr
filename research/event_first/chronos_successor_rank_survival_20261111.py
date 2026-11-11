#!/usr/bin/env python3
"""Exact rank-survival certificate for successor upper sets in finite posets.
Read-only; stdlib; bounded exhaustive enumeration through 6 elements.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import comb


def closures(n, edge_bits):
    pred = [0] * n
    k = 0
    for j in range(n):
        for i in range(j):
            if edge_bits >> k & 1:
                pred[j] |= 1 << i
            k += 1
    for j in range(n):
        for i in range(j):
            if pred[j] >> i & 1:
                pred[j] |= pred[i]
    return tuple(pred)


def first_successor_survival(pred, x):
    """Return P(B_x>j), j=0..N-1, for uniform extension of P after removing x.
    For U(x)=empty, B_x=N, so all these probabilities are 1.
    """
    n = len(pred)
    others = tuple(i for i in range(n) if i != x)
    upper = {y for y in others if pred[y] >> x & 1}
    mask_others = ((1 << n) - 1) ^ (1 << x)
    @lru_cache(None)
    def e(mask):
        if mask == mask_others:
            return 1
        return sum(e(mask | (1 << y)) for y in others
                   if not (mask >> y & 1) and not (pred[y] & ~mask & mask_others))

    den = e(0)
    frontier = {0: 1}
    survival = [F(1)]
    for j in range(1, n):
        nxt = {}
        for mask, count in frontier.items():
            for y in others:
                if not(mask >> y & 1) and not (pred[y] & ~mask & mask_others):
                    mm = mask | (1 << y)
                    nxt[mm] = nxt.get(mm, 0) + count
        frontier = nxt
        good = sum(count * e(mask) for mask, count in frontier.items()
                   if all(not(mask >> y & 1) for y in upper))
        survival.append(F(good, den))
    return survival, upper


def verify(n, mask):
    pred = closures(n, mask)
    total = 0
    for x in range(n):
        if pred[x]:
            continue
        survival, upper = first_successor_survival(pred, x)
        a = n - 1 - len(upper)
        u = len(upper)
        E = sum(survival)
        # Insertion-window formula: q_n(x) = E[min(n,B)] / E[B].
        full = (1 << n) - 1
        @lru_cache(None)
        def ep(mask):
            if mask == full: return 1
            return sum(ep(mask | (1 << v)) for v in range(n)
                       if not (mask >> v & 1) and not (pred[v] & ~mask))
        count_prefix = {0: 1}
        for cutoff in range(1, n+1):
            nxt = {}
            for mask2, count2 in count_prefix.items():
                for v in range(n):
                    if not (mask2 >> v & 1) and not (pred[v] & ~mask2):
                        m = mask2 | (1 << v)
                        nxt[m] = nxt.get(m, 0) + count2
            count_prefix = nxt
            direct = F(sum(count2*ep(mask2) for mask2,count2 in count_prefix.items()
                           if mask2 >> x & 1), ep(0))
            insert = sum(survival[:cutoff], F(0)) / E
            assert direct == insert, (n, mask, x, cutoff, direct, insert)
            if u:
                hyper = sum((F(comb(a,j),comb(n-1,j)) if j<=a else F(0))
                            for j in range(cutoff))
                assert hyper/F(a+1) <= insert
                assert insert <= min(F(1),F(min(cutoff,a+1)*(u+1),n))
        if u == 0:
            assert all(t == 1 for t in survival)
            assert E == n
        else:
            for j, s in enumerate(survival):
                lower = F(comb(a, j), comb(n-1, j)) if j <= a else F(0)
                upper_bound = F(1) if j <= a else F(0)
                assert lower <= s <= upper_bound, (n, mask, x, j, lower, s)
                total += 1
            assert E >= F(n, u+1)
            assert E <= a+1
            first_probability = 1/E
            assert F(1, a+1) <= first_probability <= F(u+1, n)
    return total


def main():
    total = 0
    for n in range(2, 7):
        count=0
        for mask in range(1 << comb(n, 2)):
            count += verify(n, mask)
        total += count
        print(f'N={n} EXACT_TAIL_COMPARISONS={count}', flush=True)
    print('TOTAL_TAIL_COMPARISONS :=',total)
    print('HYPERGEOMETRIC_SURVIVAL_DOMINATION := PASS')
    print('GENERAL_N_MINKOWSKI_SELECTION_LIMIT := OPEN')

if __name__ == '__main__':
    main()
