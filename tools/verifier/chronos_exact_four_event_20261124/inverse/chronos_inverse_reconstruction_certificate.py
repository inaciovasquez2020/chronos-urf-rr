#!/usr/bin/env python3
"""Exact rational certificate for an abstract measured causal-order counterexample.
The IVT and census identities are justified in the accompanying derivation.
No dependency on the candidate exact Minkowski M22 formula.
"""
from fractions import Fraction as Q
from itertools import product

h0,h1=Q(709,5000),Q(1419,10000)
a0,a1=Q(13,200),Q(69,1000)
assert h0**3<Q(1,350)<h1**3
k0,k1=(Q(1,10)-h1*h1)/2,(Q(1,10)-h0*h0)/2

def b(a,k): return (k-a*a)/(2*a)
def f(a,k):
    z=b(a,k)
    return 3*(a**3+3*a*a*z+a*z*z)-Q(9,350)
assert k0>a1*a1
# f increases in k for positive a,b; b decreases in a.
assert f(a0,k0)>0 and f(a1,k1)<0
b0,b1=b(a1,k0),b(a0,k1)
assert b0>0
mass_upper=h1+2*(a1+b1)
assert mass_upper<1
# Exact target census from expected comparable pairs and normalization.
chain=Q(1,350); fork=Q(9,350); pair=Q(1,10)
single=3*pair-4*fork-3*chain
anti=1-single-2*fork-chain
assert (anti,single,fork,fork,chain)==(Q(53,70),Q(33,175),Q(9,350),Q(9,350),Q(1,350))
# Four-chain separation: all four must be in the nonatomic chain.
assert h0**4>Q(1,29400)
# Common-future moment: chain contributes h^4/6; bipartite block
# contributes a^2(a+b)^2+2ab*a^2+b^2*a^2.
m22lo=h0**4/6+a0**4+4*a0**3*b0+2*a0*a0*b0*b0
assert m22lo>Q(9,10000)
# Additional independent eight-type examples: verify the complete
# directed labeled census, not merely counts of undirected edges.
from collections import Counter

def census(edges,n):
    return Counter(tuple((x[i],x[j]) in edges for i in range(n) for j in range(n) if i!=j) for x in product(range(8),repeat=n))
A={(i,4+j) for i in range(4) for j in (i,(i+1)%4)}
B={(i,4+j) for i in range(4) for j in range(4) if i//2==j//2}
assert all(census(A,n)==census(B,n) for n in (2,3))
def m22(e):
    return Q(sum(all((i,j) in e for i in (a,b) for j in (c,d)) for a,b,c,d in product(range(8),repeat=4)),8**4)
assert (m22(A),m22(B))==(Q(3,512),Q(1,128))
print('IVT_ENDPOINT_SIGNS := PASS')
print('TOTAL_MASS_UPPER :=',mass_upper)
print('THREE_EVENT_CENSUS :=',anti,single,fork,fork,chain)
print('FOUR_CHAIN_LOWER :=',h0**4)
print('FOUR_CHAIN_SEPARATION := PASS')
print('M22_LOWER :=',m22lo)
print('EIGHT_TYPE_LABELED_CENSUS_AGREEMENT := PASS')
print('EIGHT_TYPE_M22 :=',m22(A),m22(B))
print('RATIONAL_CERTIFICATE := PASS')
print('LEAN := NOT_RUN')
