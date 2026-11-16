#!/usr/bin/env python3
"""Exact rational conditional common-future offspring counts for Minkowski 4D.
Assumes the analytically derived moment formula for J | (X,Y comparable).
No sampling, Lean proof, or inference about incomparable pairs.
"""
from fractions import Fraction as Q
from math import comb

def moment(k):
    return Q(180, (k+1)**2*(k+2)**2*(2*k+1)*(2*k+3)**2*(2*k+5))

def count_prob(m,j):
    return comb(m,j)*sum(((-1)**h*comb(m-j,h)*moment(j+h) for h in range(m-j+1)), Q(0))

for m in range(21):
    probs=[count_prob(m,j) for j in range(m+1)]
    assert all(v>=0 for v in probs)
    assert sum(probs)==1
    assert sum(j*probs[j] for j in range(m+1))==Q(m,105)
    assert sum(j*(j-1)*probs[j] for j in range(m+1))==Q(m*(m-1),1764)
print('CONDITIONAL_COUNT_DISTRIBUTIONS := m=0..20 PASS')
for m in [2,3,4]:
    print('m =',m,'P(K=j|C) =', [str(count_prob(m,j)) for j in range(m+1)])
print('SOURCE := paper-derivation comparable-pair moments')
print('UNCONDITIONAL_OVERLAP := OPEN')
print('LEAN_VERIFIED := NO')
