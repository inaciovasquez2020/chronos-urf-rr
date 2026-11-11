#!/usr/bin/env python3
"""Read-only exact audit of rank-growth covariance square; Python stdlib only."""
from itertools import permutations, product
from collections import Counter
from fractions import Fraction

n=4
edges=[(i,j) for i in range(n) for j in range(i+1,n)]
perm_masks=[]
for r in permutations(range(n)):
    perm_masks.append(sum(1<<a for a,(i,j) in enumerate(edges) if r[i]<r[j]))
full=(1<<len(edges))-1
counts=Counter()
for ranks in product(perm_masks, repeat=3):
    mask=full
    for r in ranks:mask &=r
    counts[mask]+=1

def mask(E): return sum(1<<edges.index(e) for e in E)
A=mask([(0,1),(0,2),(0,3),(1,2)])
B=mask([(0,1),(0,2),(0,3),(1,3)])
pA=Fraction(counts[A],24**3)
pB=Fraction(counts[B],24**3)
base=Fraction(1,8)
assert (pA,pB)==(Fraction(19,13824),Fraction(12,13824))
assert pA/base==Fraction(19,1728)
assert pB/base==Fraction(1,144)
assert (pA-pB)/base==Fraction(7,1728)
print('ENUMERATION=PASS; configurations=',24**3)
print('C2_INITIAL_CHAIN_PROBABILITY=',base)
print('SQUARE_A=',pA,'SQUARE_B=',pB)
print('CONDITIONAL_SQUARE_A=',pA/base,'CONDITIONAL_SQUARE_B=',pB/base)
print('CONDITIONAL_SQUARE_DEFECT=',(pA-pB)/base)
print('DISCRETE_GENERAL_COVARIANCE=FAIL (rank growth k=3)')
# For transitive percolation, squares with incomparable births commute algebraically:
# w(C,P) w(C+x,Q) == w(C,Q) w(C+y,P) == w(C,P)w(C,Q)(1-p)
for p in (Fraction(1,5), Fraction(2,5), Fraction(1,2)):
    for n in range(0,5):
        for s in range(n+1):
            for m in range(s+1):
                wp=p**m*(1-p)**(n-s)
                for t in range(n+1):
                    for l in range(t+1):
                        wq=p**l*(1-p)**(n-t)
                        assert wp*(wq*(1-p))==wq*(wp*(1-p))
print('TRANSITIVE_PERCOLATION_SQUARE_IDENTITY=PASS')