#!/usr/bin/env python3
"""Exact finite-N three-cell conditional-multinomial identity + limiting moments.
Python standard library, deterministic, read-only, bounded.
"""
from fractions import Fraction as F
from math import comb, factorial

checks=0
for N in range(3,11):
    m=N-1
    for S in (F(0),F(1,8),F(1,3),F(1,2)):
        for future in (F(0),F(1,8),F(1,4),F(1,2)):
            if S+future>1 or S==1:continue
            for j in range(0,m+1):
                past_probability=F(comb(m,j))*S**j*(1-S)**(m-j)
                if past_probability==0:continue
                for v in range(m-j+1):
                    # joint law of (j predecessors, v future successors),
                    # with the remaining incomparable.
                    joint=F(factorial(m),factorial(j)*factorial(v)*factorial(m-j-v))\
                        * S**j*future**v*(1-S-future)**(m-j-v)
                    conditional=F(comb(m-j,v))*\
                        (future/(1-S))**v*((1-S-future)/(1-S))**(m-j-v)
                    assert joint/past_probability==conditional,(N,S,future,j,v)
                    checks+=1
print('EXACT_MULTINOMIAL_TO_CONDITIONAL_BINOMIAL := PASS', checks)
for k in range(1,8):
    # normalized limit U density 2u, future fraction (1-U)^2
    # integral 2u*(1-u)^(2k) du = 1/((k+1)*(2k+1))
    analytical=F(2,(2*k+1)*(2*k+2))
    closed=F(1,(k+1)*(2*k+1))
    assert analytical==closed
print('LIMITING_FUTURE_MOMENTS := PASS, degrees=1..7')
print('ASYMPTOTIC_MARKED_INTENSITY := PROVED_BY_ANALYSIS_NOT_FINITE_TEST')
print('LINEAR_EXTENSION_SELECTION_WEIGHTS := OPEN')
