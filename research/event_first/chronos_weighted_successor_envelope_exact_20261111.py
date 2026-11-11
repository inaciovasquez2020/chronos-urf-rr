#!/usr/bin/env python3
"""Exact finite-N checks and asymptotic coefficient for weighted candidate bound.
Python stdlib only, no repository writes. No numeric claim of proof.
"""
from fractions import Fraction as Q
from math import comb, pi, sqrt

# Analytic 4D diamond moments independently integrated polynomially.
Es=Q(1,20)
Es2=Q(1,105)
Esf=Q(1,2100)
assert Es2==Q(1,105) and Esf==Q(1,2100)
# N=2: isolated expected 2 E[1-s-f]; weighted all-minimal candidates=2.
assert 2*(1-2*Es)==Q(9,5)
# N=3: E[isolated]=3 E[(1-s-f)^2]
iso3=3*(1-4*Es+2*Es2+2*Esf)
# E[# min with exactly one successor]=6 E[f(1-s-f)]
one3=6*(Es-Esf-Es2)
assert iso3==Q(123,50) and one3==Q(6,25)
assert iso3+2*one3==Q(147,50)
print('EXACT_N2_ISOLATED := 9/5')
print('EXACT_N3_ISOLATED :=',iso3)
print('EXACT_N3_ONE_SUCCESSOR_MINIMA :=',one3)
print('EXACT_N3_WEIGHTED_K1 :=',iso3+2*one3)

# Fixed-K asymptotic: sum_ell (ell+1) * 3pi * binom(2ell,ell)/4^ell.
for K in (20,100,1000,10000):
    coefficient=Q(0)
    term=Q(1)
    for ell in range(K+1):
        if ell:
            term *= Q(2*(2*ell-1),4*ell)
        coefficient+=(ell+1)*term
    ratio=float(3*pi*coefficient)/(K**1.5)
    print('FIXED_K_LIMIT_COEFFICIENT_K=',K,'SCALED=',round(ratio,10),
          'TARGET=',round(2*sqrt(pi),10))
    assert 3.4 < ratio < 4.2
print('EXACT_FINITE_IDENTITIES := PASS')
print('COEFFICIENT_FORMULA := PASS')
print('GROWING_K_DOUBLE_LIMIT := ANALYTIC_PROOF_NOT_FINITE_CERTIFICATE')
print('MINKOWSKI_SELECTION_DISTRIBUTION := OPEN')
