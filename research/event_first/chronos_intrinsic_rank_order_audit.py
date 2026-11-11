#!/usr/bin/env python3
"""Exact finite audit of k-rank sequential growth. Standard library only.
No repository changes; finite enumeration N=4 only.
"""
from itertools import permutations, product
from collections import Counter
from fractions import Fraction
from math import factorial

n = 4
perms = list(permutations(range(n)))
edges = [(i,j) for i in range(n) for j in range(i+1,n)]
masks = [sum(1<<q for q,(i,j) in enumerate(edges) if r[i] < r[j]) for r in perms]
full=(1<<len(edges))-1

def mask_of(es):
    return sum(1<<edges.index(e) for e in es)

def two_plus_two(m):
    es=[e for q,e in enumerate(edges) if (m>>q)&1]
    return len(es)==2 and len(set(v for e in es for v in e))==4

def counts(k):
    out=Counter()
    for ranks in product(masks,repeat=k):
        m=full
        for a in ranks: m &= a
        out[m]+=1
    return out

A=mask_of([(0,1),(0,2),(0,3),(1,2)])
B=mask_of([(0,1),(0,2),(0,3),(1,3)])
for k in (1,2,3):
    c=counts(k)
    den=factorial(n)**k
    p22=Fraction(sum(v for m,v in c.items() if two_plus_two(m)),den)
    print(f'k={k}, d=k+1: total={sum(c.values())}, distinct_orders={len(c)}, '
          f'pair={Fraction(1,2**k)}, chain3={Fraction(1,6**k)}, '
          f'inclusive_fork3={Fraction(1,3**k)}, induced_2plus2={p22}, '
          f'covariant_history_A={Fraction(c[A],den)}, '
          f'covariant_history_B={Fraction(c[B],den)}')
    assert sum(c.values())==den
    assert c[A]!=c[B]
assert Fraction(sum(v for m,v in counts(3).items() if two_plus_two(m)),24**3)==Fraction(151,13824)
assert (counts(3)[A], counts(3)[B])==(19,12)
print('EXACT_ENUMERATION := PASS')
print('POSITIVE_2PLUS2 := PASS')
print('SEQUENTIAL_GENERAL_COVARIANCE := FAIL')
# Universal affine lower bound for any mixture over integer rank counts k>=0.
# Equality at k=3 and k=4; strict elsewhere by strict convexity
# of y=x**log_2(6) sampled on x=2**(-k).
for k in range(0,30):
    assert Fraction(1,6**k) >= Fraction(5,81)*Fraction(1,2**k)-Fraction(1,324)
assert Fraction(3,5)*Fraction(1,8)+Fraction(2,5)*Fraction(1,16)==Fraction(1,10)
assert Fraction(3,5)*Fraction(1,216)+Fraction(2,5)*Fraction(1,1296)==Fraction(1,324)
assert Fraction(1,324)-Fraction(1,350)==Fraction(13,56700)
print('INTEGER_RANK_MIXTURE_NO_GO := PROVED_ANALYTICALLY; BOUNDED_CHECK := PASS')
print('MIN_P3_AT_P2_1_OVER_10 := 1/324 > 1/350')