#!/usr/bin/env python3
"""Exact finite audit of p_a <= (|U(a)|+1)/n for 2D permutation posets."""
from itertools import permutations
from functools import lru_cache
from fractions import Fraction
from math import factorial

cases=0
minima=0
for n in range(2,9):
    count=0
    for pi in permutations(range(n)):
        pred=[sum(1<<i for i in range(j) if pi[i]<pi[j]) for j in range(n)]
        full=(1<<n)-1
        @lru_cache(None)
        def e(mask):
            if mask==0: return 1
            return sum(e(mask^(1<<i)) for i in range(n) if mask & (1<<i) and not pred[i]&mask)
        total=e(full)
        for a in range(n):
            if pred[a]:continue
            s=sum(bool(pred[j]&(1<<a)) for j in range(n))
            num=e(full^(1<<a))
            assert n*num <= (s+1)*total, (n,pi,a,s,num,total)
            count+=1
    cases+=factorial(n)
    minima+=count
    print(f'n={n} orders={factorial(n)} minimal_element_checks={count} PASS',flush=True)
print('TOTAL_ORDERS',cases)
print('TOTAL_MINIMAL_ELEMENT_CHECKS',minima)
print('FINITE_SUCCESSOR_BOUND','PASS')
print('RANDOM_ENSEMBLE_COLLISION_DECAY','OPEN')