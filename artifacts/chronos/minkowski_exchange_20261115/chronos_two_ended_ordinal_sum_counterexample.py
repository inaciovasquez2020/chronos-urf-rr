#!/usr/bin/env python3
"""Exact finite checks for the chain-below-antichain endpoint counterexample.

No asymptotic probabilistic claim about random permutation orders is made.
Python 3 standard library only.
"""
from fractions import Fraction
from functools import lru_cache
from math import factorial


def endpoint_stats(pi):
    n = len(pi)
    pred = [sum(1 << j for j in range(i) if pi[j] < pi[i]) for i in range(n)]
    successors = [sum(1 << j for j in range(i+1, n) if pi[i] < pi[j]) for i in range(n)]
    full = (1 << n) - 1

    @lru_cache(None)
    def extensions(mask):
        if mask == 0:
            return 1
        return sum(extensions(mask ^ (1 << i)) for i in range(n)
                   if mask & (1 << i) and not (pred[i] & mask))

    total = extensions(full)
    mins = [i for i in range(n) if pred[i] == 0]
    maxs = [i for i in range(n) if successors[i] == 0]
    first = [Fraction(extensions(full ^ (1 << i)), total) for i in mins]
    last = [Fraction(extensions(full ^ (1 << j)), total) for j in maxs]
    joint = [Fraction(extensions(full ^ (1 << i) ^ (1 << j)), total)
             for i in mins for j in maxs if i != j]
    assert sum(first) == sum(last) == sum(joint) == 1
    return sum(p*p for p in first), sum(q*q for q in last), sum(r*r for r in joint), total


def run():
    print('MODEL := ordinal sum Chain(L) < Antichain(m)')
    for L,m in [(2,3),(3,5),(5,6),(7,7)]:
        pi = tuple(range(L)) + tuple(range(L+m-1,L-1,-1))
        cp,cm,j,num = endpoint_stats(pi)
        assert (cp,cm,j,num) == (Fraction(1),Fraction(1,m),Fraction(1,m),factorial(m))
        dual = tuple(len(pi)-1-pi[len(pi)-1-i] for i in range(len(pi)))
        cp2,cm2,j2,num2 = endpoint_stats(dual)
        assert (cp2,cm2,j2,num2) == (Fraction(1,m),Fraction(1),Fraction(1,m),factorial(m))
        print(f'L={L} m={m} n={L+m} first={cp} last={cm} joint={j} extensions={num} dual=PASS')
    print('EXACT_FINITE_CHECK := PASS')
    print('DETERMINISTIC_LIMIT := follows from closed forms as m tends to infinity')
    print('RANDOM_ENSEMBLE_COLLISION_DECAY := OPEN')

if __name__ == '__main__':
    run()