#!/usr/bin/env python3
"""Exact null-coordinate endpoint and normalization audit for Chronos B.

No claim of evaluation of the global four-event integral.
"""
from fractions import Fraction as F
from random import Random
import sympy as S

U,V,P,Q,a = S.symbols('U V P Q a', positive=True)
Tx=(U+V)/2; Ty=(P+Q)/2
r=(V-U)/2; w=(Q-P)/2
bminus=S.factor((Tx*Ty-r*w)/a)
bplus=S.factor((Tx*Ty+r*w)/a)
assert S.simplify(bminus-(U*Q+V*P)/(2*a))==0
assert S.simplify(bplus-(U*P+V*Q)/(2*a))==0
assert S.simplify((Tx*w-Ty*r)-(U*Q-V*P)/2)==0
assert S.simplify((Tx*w+Ty*r)-(V*Q-U*P)/2)==0
assert S.expand((U*Q+V*P)**2-4*U*V*P*Q-(U*Q-V*P)**2)==0
assert S.expand((U*P+V*Q)**2-4*U*V*P*Q-(V*Q-U*P)**2)==0
assert S.expand(U*V+P*Q-U*Q-V*P-(U-P)*(V-Q))==0
assert S.expand(U*V+P*Q-U*P-V*Q-(U-Q)*(V-P))==0
assert F(96,1)*F(1,4)*F(1,2)==12
assert S.integrate(S.integrate(12*(V-U)**2,(U,0,V)),(V,0,1))==1
assert F(4608)*F(1,2)**2*F(1,2)**2==288

rng=Random(20261121)
cases=0
counter={'bminus_timelike':0,'bminus_spacelike':0,'bplus_timelike':0,'bplus_spacelike':0}
for _ in range(2000):
    p=sorted((F(rng.randint(1,999),1000),F(rng.randint(1,999),1000)))
    q=sorted((F(rng.randint(1,999),1000),F(rng.randint(1,999),1000)))
    uu,vv=p; pp,qq=q
    if uu==vv or pp==qq: continue
    a2=uu*vv; c2=pp*qq
    bm_num=uu*qq+vv*pp
    bp_num=uu*pp+vv*qq
    dm_num=abs(uu*qq-vv*pp)
    dp_num=vv*qq-uu*pp
    assert bm_num*bm_num-dm_num*dm_num==4*a2*c2
    assert bp_num*bp_num-dp_num*dp_num==4*a2*c2
    assert bm_num-dm_num==2*min(uu*qq,vv*pp)
    assert bp_num-dp_num==2*uu*pp
    sign_minus=bm_num-(a2+c2)
    sign_plus=bp_num-(a2+c2)
    assert sign_minus==-(uu-pp)*(vv-qq)
    assert sign_plus==-(uu-qq)*(vv-pp)
    counter['bminus_timelike' if sign_minus<=0 else 'bminus_spacelike']+=1
    counter['bplus_timelike' if sign_plus<=0 else 'bplus_spacelike']+=1
    cases+=1
assert cases>=1900
assert all(counter.values()),counter
print('SYMBOLIC_NULL_ENDPOINT_FACTORIZATIONS := PASS')
print('NULL_DENSITY_NORMALIZATION := PASS')
print('ANGULAR_JACOBIAN := PASS')
print('EXACT_RATIONAL_ENDPOINT_CHECKS :=',cases)
print('BRANCH_COUNTS :=',counter)
print('FOUR_DIMENSIONAL_NULL_KERNEL := B = 288 Integral_(0<U<V<1,0<P<Q<1) sqrt(U*V)*(V-U)*(Q-P)*I(a,c;bminus,bplus) dU dV dP dQ')
print('bminus := (U*Q+V*P)/(2*sqrt(U*V))')
print('bplus := (U*P+V*Q)/(2*sqrt(U*V))')
print('zminus := min(U*Q,V*P)/sqrt(U*V)')
print('zplus := U*P/sqrt(U*V)')
print('TIMELIKE_BRANCH_TEST := (U-P)*(V-Q) >= 0 for bminus')
print('GLOBAL_B := OPEN')
print('GLOBAL_P42 := OPEN')
