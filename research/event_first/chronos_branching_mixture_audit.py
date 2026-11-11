#!/usr/bin/env python3
"""Exact audit of a two-component Bayesian mixture of transitive percolation.
All calculations are rational and bounded at five events.
"""
from fractions import Fraction as F
from math import comb

ps=(F(1,10),F(3,10))
alpha=(F(1,2),F(1,2))

def downs(state):
    n=len(state)
    for pr in range(1<<n):
        if all((pr & state[i])==state[i] for i in range(n) if (pr>>i)&1):
            yield pr

def maximal(state,pr):
    return sum(bool(pr & (1<<i)) and not any((pr & (1<<j)) and (state[j] & (1<<i)) for j in range(len(state))) for i in range(len(state)))

def invariants(state):
    n=len(state)
    I=comb(n,2)-sum(p.bit_count() for p in state)
    L=sum(maximal(state,p) for p in state)
    return L,I

def H(state):
    L,I=invariants(state)
    return sum((a*p**L*(1-p)**I for a,p in zip(alpha,ps)),F(0))

def w(state,pr):
    return H(state+(pr,))/H(state)

states={():F(1)}
for n in range(5):
    next_states={}
    checks=0
    for s,prob in states.items():
        T=list(downs(s)); assert sum((w(s,pr) for pr in T),F(0))==1
        for a in T:
            for b in T:
                lhs=w(s,a)*w(s+(a,),b)
                rhs=w(s,b)*w(s+(b,),a)
                assert lhs==rhs
                checks+=1
            next_states[s+(a,)]=next_states.get(s+(a,),F(0))+prob*w(s,a)
    assert sum(next_states.values(),F(0))==1
    states=next_states
    print('SIZE',n+1,'STATES',len(states),'COVARIANCE_SQUARES',checks)

p2=sum((a*p for a,p in zip(alpha,ps)),F(0))
p3=sum((a*p*p for a,p in zip(alpha,ps)),F(0))
assert p2==F(1,5) and p3==F(1,20)
assert p3>p2*p2
q=[1-p for p in ps]
r_one=sum((a*x for a,x in zip(alpha,q)),F(0))/sum((a*x for a,x in zip(alpha,ps)),F(0))
r_two=sum((a*x**3 for a,x in zip(alpha,q)),F(0))/sum((a*ps[i]*q[i]**2 for i,a in enumerate(alpha)),F(0))
assert r_one==4 and r_two==F(268,57) and r_two!=r_one
print('P2_FIRST_TWO :=',p2)
print('P3_FIRST_THREE :=',p3)
print('BELL_SPECTATOR_RATIOS :=',r_one,r_two)
print('BELL_CAUSALITY := FAIL')
print('NORMALIZATION_DGC := PASS')