#!/usr/bin/env python3
"""Exact five-birth CSG obstruction for the certified common-N=4 coupling box.
Python 3.9+ stdlib; read-only; all computations rational.
The supplied 4-event existence certificate independently establishes that the
exact common-four-event solution lies inside BOX below.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import defaultdict
from math import comb

CENTER=(F(684064,100000000),F(222049,10000000),F(17390282,100000000))
RAD=F(1,100000)
LO=tuple(c-RAD for c in CENTER)
HI=tuple(c+RAD for c in CENTER)
TARGET=(F(1,10),F(1,350),F(1,29400))
assert all(v>0 for v in LO)

def ideals(p):
    for mask in range(1<<len(p)):
        if all((mask&p[i])==p[i] for i in range(len(p)) if mask>>i&1):
            yield mask

def transition(p,mask,t):
    n=len(p)
    w=bin(mask).count('1')
    m=sum(1 for i in range(n) if (mask>>i)&1 and not any(
        (mask>>j)&1 and (p[j]>>i)&1 for j in range(n)))
    return sum(F(comb(w-m,k-m))*t[k] for k in range(m,w+1))

def grow4(xyz):
    t=(F(1),)+tuple(xyz)
    states={():F(1)}
    for n in range(4):
        nxt=defaultdict(F)
        for p,mass in states.items():
            for a in ideals(p):nxt[p+(a,)]+=mass*transition(p,a,t)
        states=dict(nxt)
        assert len(states)==(1,2,7,40)[n]
        normal=F(1)
        for j in range(n+1):
            normal*=sum(comb(j,k)*t[k] for k in range(j+1))
        assert sum(states.values())==normal
    return states

def chain_density(p,k):
    n=len(p)
    count=0
    for subset in combinations(range(n),k):
        if all((p[j]>>i)&1 for i,j in combinations(subset,2)):
            count+=1
    return F(count,comb(n,k))

def coefficients(xyz):
    t=(F(1),)+tuple(xyz)+(F(0),)
    states=grow4(xyz)
    numer=[[F(0),F(0)] for _ in range(3)]
    denom=[F(0),F(0)]
    terminal=set()
    for p,mass in states.items():
        for a in ideals(p):
            q=p+(a,)
            terminal.add(q)
            weights=(transition(p,a,t),F(int(a==15)))
            for j,w in enumerate(weights):
                denom[j]+=mass*w
                for i,k in enumerate((2,3,4)):
                    numer[i][j]+=mass*w*chain_density(q,k)
    assert len(terminal)==357
    assert denom[1]==sum(states.values())
    x,y,z=xyz
    assert denom[0]==denom[1]*(1+4*x+6*y+4*z)
    return numer,denom

nlo,dlo=coefficients(LO)
nhi,dhi=coefficients(HI)
nmid,dmid=coefficients(CENTER)
for j in range(2):
    assert dlo[j]<=dmid[j]<=dhi[j]
for i in range(3):
    for j in range(2):assert nlo[i][j]<=nmid[i][j]<=nhi[i][j]

# Each numerator/denominator coefficient is a polynomial in x,y,z
# with NONNEGATIVE coefficients, so endpoint evaluation brackets every
# parameter point in the prior certified positive 3D coupling box.
# Any w=t4>=0 then obeys N(w) >= Nlo0+w*Nlo1 and
# D(w) <= Dhi0+w*Dhi1.
LOWER=(F(19,100),F(1,50),F(7,10000))
for i,k in enumerate((2,3,4)):
    margin0=nlo[i][0]-LOWER[i]*dhi[0]
    margin1=nlo[i][1]-LOWER[i]*dhi[1]
    assert margin0>0 and margin1>0,(k,margin0,margin1)
    assert LOWER[i]>TARGET[i]
    print('CHAIN',k,'TARGET',TARGET[i], 'UNIFORM_CERTIFIED_STRICT_LOWER',LOWER[i])
    print('  COEFFICIENT_GAP_AT_T4_0_GT',margin0>0,
          'COEFFICIENT_GAP_AT_T4_INFINITY_GT',margin1>0)
    print('  CENTER_T4_ZERO',format(float(nmid[i][0]/dmid[0]),'.12g'),
          'CENTER_T4_INFINITY',format(float(nmid[i][1]/dmid[1]),'.12g'))

# Independent normalization test with t4=1/7, avoiding symbolic
# denominator assumptions about the fifth step.
test_t4=F(1,7)
num,den=coefficients(CENTER)
observed=[(q[0]+test_t4*q[1])/(den[0]+test_t4*den[1]) for q in num]
assert all(a>t for a,t in zip(observed,TARGET))
print('N5_NATURALLY_LABELED_STATES := 357')
print('NONNEGATIVE_COUPLING_BOX_AUDIT := PASS')
print('T4_FREE_NONNEGATIVE := ALL_THREE_TARGETS_IMPOSSIBLE')
print('ORIGINAL_FOUR_EVENT_BOX := ASSUMED_PREVIOUSLY_CERTIFIED')
print('FINITE_FIVE_EVENT_OBSTRUCTION := PROVED_CONDITIONALLY_ON_FOUR_EVENT_CERTIFICATE')
print('MAC := NOT_RUN; LEAN := NOT_RUN; REPOSITORY := UNCHANGED_BY_SCRIPT')
