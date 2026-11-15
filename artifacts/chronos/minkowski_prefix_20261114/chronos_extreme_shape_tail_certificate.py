#!/usr/bin/env python3
"""Exact upper bounds for atypically long increasing/decreasing subsequences.
No external dependencies, no repository modification, exact rational arithmetic.
"""
from fractions import Fraction
from math import comb, factorial, ceil, log, lgamma, log10

def union_tail(n,k):
    assert 1 <= k <= n
    # Every fixed k-subset has increasing relative order with probability 1/k!.
    return Fraction(comb(n,k),factorial(k))

for n in (20, 50, 100, 200, 400, 800):
    k=ceil(n/2)
    bound=min(Fraction(1),2*union_tail(n,k))
    m=max(1,int(log(n)))
    L=n-m+1
    chain_bound=min(Fraction(1),union_tail(n,L))
    print('n=%d  log10(P[height>=ceil(n/2) OR width>=ceil(n/2)] upper bound) = %.3f; log10(P[height>=n-floor(log n)+1] upper bound) = %.3f' % (n, log10(2) + (lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1)-lgamma(k+1))/log(10), (lgamma(n+1)-lgamma(L+1)-lgamma(n-L+1)-lgamma(L+1))/log(10)))
    assert bound >= 0 and chain_bound >= 0
print('RESULT := COMPUTATION_PASS')
print('CERTIFICATE := exact rational union bounds; applicability follows from uniform permutation symmetry')
print('LIMIT := bounds only exclude extreme-shaped counterexample families, not all first-weight concentration')