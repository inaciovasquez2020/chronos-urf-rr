#!/usr/bin/env python3
"""Exact finite verification of chain-plus-isolates permutation-poset family."""
from functools import lru_cache
from fractions import Fraction
from math import comb

def extension_counts(permutation):
    n=len(permutation)
    preds=tuple(sum(1<<i for i in range(j) if permutation[i]<permutation[j]) for j in range(n))
    @lru_cache(None)
    def ext(mask):
        if not mask:return 1
        return sum(ext(mask^(1<<i)) for i in range(n) if mask>>i&1 and preds[i]&mask==0)
    full=(1<<n)-1
    e=ext(full)
    first={i:ext(full^(1<<i)) for i in range(n) if preds[i]==0}
    collision=sum(Fraction(x*x,e*e) for x in first.values())
    comparable=sum(Fraction(ext(full^(1<<i)^(1<<j)),e) for i in first for j in range(n) if preds[j]==1<<i)
    return e,first,collision,comparable

for n,m in [(6,3),(8,4),(10,3),(12,5)]:
    L=n-m+1
    pi=tuple(range(n,n-m+1,-1))+tuple(range(1,L+1))
    e,first,C,A=extension_counts(pi)
    assert e==comb(n,m-1)*__import__('math').factorial(m-1)
    assert len(first)==m
    assert A==Fraction(L*(L-1),n*(n-1))
    assert C==Fraction(L*L+m-1,n*n)
    print(f'n={n} m={m} permutation={pi} extensions={e} prefix={A} collision={C}')
print('RESULT := COMPUTATION_PASS')
print('GENERAL_FAMILY_THEOREM := mathematical combinatorial proof required, not Lean-verified')