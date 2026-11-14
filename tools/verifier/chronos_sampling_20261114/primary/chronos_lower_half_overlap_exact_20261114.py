#!/usr/bin/env python3
"""Exact lower-half common-future volume for incomparable pairs in the 4D diamond.
Standalone geometric lemma, not a complete Minkowski four-point integral.
"""
from fractions import Fraction as F
from random import Random
from math import sqrt
from scipy.integrate import quad


def exact_lower_half(t, s, d):
    t,s,d = F(t),F(s),F(d)
    assert 0<=t<=F(1,2) and 0<=s<=F(1,2)
    assert d>abs(t-s) and d<=t+s # spacelike separated, spatial radius feasibility
    h=max(F(0),1-t-s-d)
    return (d*d-(t-s)**2)*h**3/d + h**4/F(2)


def numerical_lens(t,s,d):
    a=(t+s+d)/2
    if a>=0.5: return 0.0
    def integrand(tau):
        r1=tau-t; r2=tau-s
        v=(r1+r2-d)**2*(d*d+2*d*(r1+r2)-3*(r1-r2)**2)/(12*d)
        return 24*v # 24/pi times pi* polynomial/12d
    return quad(integrand, a, 0.5, epsabs=1e-12)[0]

rng=Random(20261114)
checks=0; nonzero=0; zero=0
for _ in range(1000):
    # Exact rational radii not needed: use directly rational t,s,d satisfying spacelike triangle.
    t=F(rng.randint(1,48),100)
    s=F(rng.randint(1,48),100)
    low=abs(t-s)
    high=t+s
    if high<=low: continue
    v=F(rng.randint(1,99),100)
    d=low+(high-low)*v
    ex=exact_lower_half(t,s,d)
    nq=numerical_lens(float(t),float(s),float(d))
    assert abs(float(ex)-nq)<1e-11,(t,s,d,ex,nq)
    assert ex>=0
    nonzero += bool(ex)
    zero += not bool(ex)
    checks+=1

assert checks==1000 and nonzero>0 and zero>0
print('EXACT_FORMULA := [(d^2-(t-s)^2)/d]*h^3 + h^4/2')
print('h := max(0,1-t-s-d), t,s<=1/2, |t-s|<d<=t+s')
print('NUMERIC_LENS_INDEPENDENT_CHECKS :=',checks)
print('POSITIVE_CASES :=',nonzero,'ZERO_CASES :=',zero)
print('LOWER_HALF_OVERLAP_IDENTITY := COMPUTATION_PASS')
print('FULL_COMMON_FUTURE_MOMENT := OPEN')
