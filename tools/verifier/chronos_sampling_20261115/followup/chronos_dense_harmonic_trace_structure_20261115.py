#!/usr/bin/env python3
"""Exact-arithmetic checks for Chronos bivariate radial coordinate completeness.
The infinite-dimensional Stone-Weierstrass argument is in the accompanying proof.
No computed angular traces or p42 value is claimed.
"""
from fractions import Fraction as Q
from itertools import product

def uv(a,b):
    return (a*b)**2,((1-a)*(1-b))**2

a,b=Q(1,8),Q(1,2)
c,d=Q(1,10),Q(5,8)
assert 0<a<b<1 and 0<c<d<1
u,v=uv(a,b);u2,v2=uv(c,d)
assert u==u2 and v!=v2
checks=0
for aa,bb in product(range(1,15),repeat=2):
    if aa>=bb:continue
    a,b=Q(aa,16),Q(bb,16)
    u,v=uv(a,b)
    p=a*b;q=(1-a)*(1-b)
    assert u==p*p and v==q*q
    s=1+p-q
    assert s==a+b and a*a-s*a+p==0 and b*b-s*b+p==0
    jac=b-a
    assert jac>0
    checks+=1
assert checks==91,checks
print('U_ALONE_NOT_INJECTIVE := PASS')
print('BIVARIATE_RECONSTRUCTION := 91/91 PASS')
print('INTERIOR_JACOBIAN_NONZERO := 91/91 PASS')
print('DENSE_BASIS_THEOREM := ANALYTIC (see report)')
print('MIXED_BASIS_ENERGY := NOT_RUN')
print('EXACT_P42 := OPEN')
print('LEAN_VERIFIED := NOT_RUN')
