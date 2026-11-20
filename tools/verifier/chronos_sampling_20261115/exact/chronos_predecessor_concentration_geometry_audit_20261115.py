#!/usr/bin/env python3
"""Independent exact-rational checks of the geometric overlap lemma and
one-point null-coordinate moment normalization. Not a Lean verification,
not a finite computational proof of asymptotic concentration.
"""
from fractions import Fraction as Q
from math import comb
from random import Random

# Density in (a,b): 12 (b-a)^2, 0<=a<=b<=1.
# W_-=(a*b)^2. Integrate polynomial over the ordered triangle exactly.
def wmoment(k):
    return 12 * (Q(1,2*k+1)-Q(2,2*k+2)+Q(1,2*k+3)) / (4*k+4)
assert wmoment(0)==1
assert wmoment(1)==Q(1,20)
assert wmoment(2)==Q(1,105)
assert wmoment(3)==Q(1,336)

# Algebraic identity: Minkowski separation of (t,r*n) and (tau,rho*m)
# equals factored expression in a=t-r, b=t+r, u=tau-rho, v=tau+rho
# plus an angular penalty -2r*rho*(1-cos(theta)).
for a,b,u,v,c in [
    (Q(1,13),Q(5,7),Q(1,40),Q(1,3),Q(1,5)),
    (Q(1,100),Q(7,8),Q(1,300),Q(2,5),Q(-1,3)),
    (Q(1,30),Q(5,6),Q(1,60),Q(1,4),Q(0)),
]:
    t,r=(a+b)/2,(b-a)/2
    tau,rho=(u+v)/2,(v-u)/2
    lhs=(t-tau)**2-r*r-rho*rho+2*r*rho*c
    rhs=(a-u)*(b-v)-2*r*rho*(1-c)
    assert lhs==rhs

# A bound on common-past events based on the angular separation.
# For gamma=pi, delta=1-cos(gamma/2)=1. At least one of the two
# directional cosine gaps 1-n_i.dot(m) >=1 for opposite n_i.
# Test exact sign of causal inequality and the resulting rho cap for
# randomly sampled rational points satisfying individual causal past.
rng=Random(20261115)
checks=0
for _ in range(25000):
    b=Q(rng.randint(40,90),100)
    a=Q(rng.randint(1,15),1000)
    t,r=(a+b)/2,(b-a)/2
    rho=Q(rng.randint(0,1000),10000)
    u=Q(rng.randint(0,150),10000)
    tau=rho+u
    # n1=+axis; n2=-axis; test direction m with cosine c to +axis.
    c=Q(rng.randint(-100,100),100)
    if tau>t:continue
    for ci in (c,-c):
        sep=(t-tau)**2-(r*r+rho*rho-2*r*rho*ci)
        if sep>=0 and 0<=u<=a and tau<=t and tau>=rho:
            assert 2*r*rho*(1-ci) <= a*b
            if 1-ci>=1:
                assert rho <= a*b/(2*r)
            checks+=1
print('RATIONAL_NULL_MOMENTS := 4/4 PASS')
print('MINKOWSKI_CAUSAL_FACTORIZATION := 3/3 PASS')
print('VALID_CAUSAL_GEOMETRY_CHECKS :=',checks)
print('L2_CONCENTRATION := ANALYTIC_ARGUMENT_IN_COMPANION_REPORT')
print('WEIGHT_RATIO_SCALING := OPEN')
print('LEAN_VERIFIED := NOT_RUN')
