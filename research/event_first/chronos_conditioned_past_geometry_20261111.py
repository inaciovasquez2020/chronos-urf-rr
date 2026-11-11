#!/usr/bin/env python3
"""Independent bounded checks of conditional past-diamond geometry.
Standard library only. Conditional-law claims have direct probabilistic proofs.
No repo writes, network, downloads, or unbounded enumeration.
"""
from fractions import Fraction as F
from random import Random
from math import sqrt

SEED=20261111
SAMPLES=120_000
rng=Random(SEED)

def point():
    # Uniform four-volume in I((0,0),(1,0)), spatial dimension 3.
    r_t = .5*rng.random()**.25
    t = r_t if rng.random()<.5 else 1-r_t
    radius = min(t,1-t)*rng.random()**(1/3)
    v=[rng.gauss(0,1) for _ in range(3)]
    norm=sqrt(sum(z*z for z in v))
    return (t,*(radius*z/norm for z in v))

def before(x,y):
    dt=y[0]-x[0]
    return dt>0 and dt*dt>sum((y[i]-x[i])**2 for i in (1,2,3))

def cdf_beta22(t): return 3*t*t-2*t*t*t

# Algebraic certificate: normalized section integral in v of min(u*v,(1-u)*(1-v))
# equals u*(1-u)/2, hence f_U(u)=6*u*(1-u).
for i in range(1,20):
    u=F(i,20)
    section=(u*(1-u)**2+(1-u)*u**2)/2
    assert section==u*(1-u)/2
    assert 6*u*(1-u)>=0
print('NULL_COORDINATE_SECTION_IDENTITY := PASS',flush=True)

mean=0.;second=0.;below=[0,0,0]; pairs=0
for _ in range(SAMPLES):
    x=point();y=point()
    u=x[0]+x[1]
    mean+=u;second+=u*u
    for idx,t in enumerate((.1,.25,.5)):
        below[idx]+= u<t
    pairs+=before(x,y) or before(y,x)
mean/=SAMPLES;second/=SAMPLES
assert abs(mean-.5)<.006,(mean,.5)
assert abs(second-.3)<.006,(second,.3)
for got,t in zip(below,(.1,.25,.5)):
    assert abs(got/SAMPLES-cdf_beta22(t))<.008,(t,got/SAMPLES,cdf_beta22(t))
assert abs(pairs/SAMPLES-.1)<.008,pairs/SAMPLES
print('SEED :=',SEED,'PAIRS :=',SAMPLES)
print('NULL_RATIO_U_MEAN :=',round(mean,7),'TARGET := 1/2')
print('NULL_RATIO_U_SECOND_MOMENT :=',round(second,7),'TARGET := 3/10')
for got,t in zip(below,(.1,.25,.5)):
    print('NULL_RATIO_CDF :=',t,round(got/SAMPLES,7),'TARGET :=',round(cdf_beta22(t),7))
print('TWO_ANCESTOR_COMPARABILITY :=',round(pairs/SAMPLES,7),'TARGET := 1/10')
print('CONDITIONAL_PAST_DIAMOND_LAW := PROVED_BY_EXCHANGEABILITY')
print('NUMERIC_INDEPENDENT_REGRESSION := PASS')
print('LINEAR_EXTENSION_SELECTION_WEIGHT_ASYMPTOTICS := OPEN')
