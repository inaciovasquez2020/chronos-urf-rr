#!/usr/bin/env python3
"""Exact analytic moment identities and probability lower bound, no Lean claim.

Assumptions: four i.i.d. uniform points in a 4D Minkowski causal diamond.
J(X,Y) is the diamond-normalized common-future volume of X and Y.
Validates a new rigorous lower bound but NOT exact E[J^2] or the prefix limit.
"""
from fractions import Fraction as F
from math import comb
from itertools import product, combinations

def moment(r, s):
    # Null coordinates 0 <= a <= b <= 1, measure 12(b-a)^2 da db.
    # W_-=a^2 b^2, W_+=(1-a)^2(1-b)^2.
    total=F(0)
    for i in range(2*s+1):
        for j in range(2*s+1):
            for k, c in enumerate((1,-2,1)):
                total+=F(12*(-1)**(i+j)*comb(2*s,i)*comb(2*s,j)*c,
                         (2*r+i+k+1)*(4*r+i+j+4))
    return total

assert moment(0,0)==1
assert moment(1,0)==moment(0,1)==F(1,20)
assert moment(2,0)==moment(0,2)==F(1,105)
assert moment(1,1)==F(1,2100)
assert moment(1,2)==moment(2,1)==F(1,35280)

# Symmetry and conditioning on a third uniform event Z:
# E[J] = P(X<Z,Y<Z) = E[W_-^2]
EJ=moment(2,0)
# For X<Y, their common future equals the future of Y.
# Integration over X gives W_-(Y), hence orientation contribution M_(1,2).
EJ_comp=2*moment(1,1)
EJ2_comp=2*moment(1,2)
Pcomp=2*moment(1,0)
assert EJ==F(1,105)
assert EJ_comp==F(1,1050)
assert EJ2_comp==F(1,17640)
assert Pcomp==F(1,10)
EJ_incomp=EJ-EJ_comp
Pincomp=1-Pcomp
assert EJ_incomp==F(3,350)
assert Pincomp==F(9,10)
# Conditional Cauchy Schwarz on incomparable event:
# E[J^2;incomp] >= E[J;incomp]^2 / P(incomp).
lower=EJ2_comp+EJ_incomp**2/Pincomp
assert lower==F(61,441000)

print('MOMENT_NORMALIZATION := PASS')
print('E[J] :=',EJ)
print('E[J;COMPARABLE] :=',EJ_comp)
print('E[J^2;COMPARABLE] :=',EJ2_comp)
print('E[J;INCOMPARABLE] :=',EJ_incomp)
print('P(INCOMPARABLE) :=',Pincomp)
print('RIGOROUS_LOWER_BOUND_E[J^2] :=',lower)
print('RIGOROUS_LOWER_BOUND_DECIMAL :=',float(lower))
print('EXACT_E[J^2] := OPEN')
print('MINKOWSKI_PREFIX_UNIQUENESS := OPEN')
print('LEAN_VERIFIED := NO')
