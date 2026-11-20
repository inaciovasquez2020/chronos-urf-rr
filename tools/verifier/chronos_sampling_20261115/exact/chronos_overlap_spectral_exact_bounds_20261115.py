#!/usr/bin/env python3
"""Reproducible exact rational spectral bounds for E[J_+^2] and p_(4,2).

Domain: four i.i.d. events uniformly sampled from the unit 4D Minkowski
Alexandrov diamond. Integrates the degree-zero spherical harmonic exactly,
and uses the trace/Hilbert-Schmidt estimate for all higher harmonics.
No Lean proof, no full exact evaluation of E[J_+^2], and no growth limit.
Python standard library only.
"""
from fractions import Fraction as Q
from itertools import permutations
from collections import defaultdict
from math import factorial, prod


def ordered_simplex_gap_integral(factors, n):
    """Integrate product of (x_j-x_i) over 0<x_0<...<x_(n-1)<1.

    Each (i,j) has 0<=i<j<n. Exact Dirichlet gap integration.
    """
    poly={(0,)*(n-1):1}
    for i,j in factors:
        assert 0<=i<j<n
        nxt=defaultdict(int)
        for mon,co in poly.items():
            for k in range(i,j):
                powers=list(mon);powers[k]+=1
                nxt[tuple(powers)]+=co
        poly=nxt
    degree=len(factors)
    numerator=sum(co*prod(factorial(k) for k in powers) for powers,co in poly.items())
    return Q(numerator,factorial(n+degree))


def mode_zero_for_graph(n,edges):
    """Exact angular l=0 piece for graph with degrees <=2, n<=4.

    Graph is directed from lower events i to upper events j; density of
    each (a_i,b_i) is 12(b_i-a_i)^2. Causality angular eigenvalue l=0
    is 1 on separated null intervals and
    (a_j-a_i)(b_j-b_i)/((b_i-a_i)(b_j-a_j)) on overlapping intervals.
    """
    total=Q(0);valid=0
    items=tuple((i,side) for i in range(n) for side in (0,1))
    for order in permutations(items):
        at={x:k for k,x in enumerate(order)}
        if any(at[i,0]>=at[i,1] for i in range(n)):continue
        if any(at[i,0]>=at[j,0] or at[i,1]>=at[j,1] for i,j in edges):continue
        leftover=[2]*n; factors=[]
        for i,j in edges:
            if at[i,1]<at[j,0]:continue
            assert at[i,0]<at[j,0]<at[i,1]<at[j,1]
            leftover[i]-=1;leftover[j]-=1
            factors.extend([(at[i,0],at[j,0]),(at[i,1],at[j,1])])
        if any(k<0 for k in leftover):raise ValueError('angular degree > 2')
        for i,k in enumerate(leftover):
            factors.extend([(at[i,0],at[i,1])]*k)
        assert len(factors)==2*n
        total+=12**n*ordered_simplex_gap_integral(factors,2*n)
        valid+=1
    return total,valid

# Normalize angular kernel to the established exact 4D causal moments.
assert mode_zero_for_graph(2,[(0,1)])==(Q(1,20),2)
assert mode_zero_for_graph(3,[(0,2),(1,2)])==(Q(1,105),16)
assert mode_zero_for_graph(3,[(0,1),(0,2)])==(Q(1,105),16)

# Angular degree-zero contribution to E[J_+^2] is the K_(2,2) four-cycle.
A0,orders=mode_zero_for_graph(4,[(0,2),(0,3),(1,2),(1,3)])
assert orders==152 and A0==Q(513,875875)

# Hilbert-Schmidt norm-square b0 of angular l=0 causal kernel,
# involving only a single directed causal relation X<Y.
# Cases ac<bc<ay<by (full angular causal) and ac<ay<bc<by (partial).
full=144*ordered_simplex_gap_integral([(0,1)]*2+[(2,3)]*2,4)
part=144*ordered_simplex_gap_integral([(0,1)]*2+[(2,3)]*2,4)
assert full==part==Q(1,70)
b0=full+part
assert b0==Q(1,35)

# The kernel 1_{X<Y} has total normalized Hilbert-Schmidt mass
# ∑_l (2l+1)*b_l = Pr(X<Y) = 1/20.
# By angular decomposition and positivity:
# E[J^2] = ∑_l A_l with A_l=(2l+1)*Tr((K_l K_l*)^2)>=0,
# and A_l <= (2l+1)*b_l^2.
# All l>=1 have multiplicity >=3, so the upper bound is
# A0 + (sum_{l>=1}(2l+1)*b_l)^2/3.
remainder_mass=Q(1,20)-b0
assert remainder_mass==Q(3,140)
J_low=A0
J_high=A0+remainder_mass**2/3
assert J_high==Q(1479,2002000)

# Independently established exact four-poset relation:
# p_(4,2) = 3557/42000 + 6*E[J^2]/5.
p_low=Q(3557,42000)+Q(6,5)*J_low
p_high=Q(3557,42000)+Q(6,5)*J_high
assert p_low==Q(17950529,210210000)
assert p_high==Q(2569877,30030000)
print('NORMALIZATION_TESTS := PASS (1 edge and both 3-event forks)')
print('ANGULAR_ZERO_ORDERED_INTERVALS :=',orders)
print('ANGULAR_ZERO_E_J2 :=',J_low)
print('ANGULAR_CAUSAL_KERNEL_HS0 :=',b0)
print('TOTAL_HIGHER_HARMONIC_HS_MASS :=',remainder_mass)
print('RIGOROUS_J2_INTERVAL :=',J_low, '<= E[J^2] <=',J_high)
print('RIGOROUS_P42_INTERVAL :=',p_low, '<= p42 <=',p_high)
print('RIGOROUS_P42_INTERVAL_WIDTH :=',p_high-p_low)
print('EXACT_J2_VALUE := OPEN')
print('INFINITE_GROWTH_STABILITY := OPEN')
print('LEAN_VERIFIED := NOT_RUN')
