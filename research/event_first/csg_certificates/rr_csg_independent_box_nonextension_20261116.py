#!/usr/bin/env python3
"""Exact CSG 4-to-5 coefficient certificate (stdlib Python 3.9+).
Proves uniform inequalities on the rational coupling box for all t4 >= 0.
Does NOT establish global uniqueness of the 4-event target solution.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import comb

ZERO={}
ONE={(0,0,0):F(1)}
X={(1,0,0):F(1)}
Y={(0,1,0):F(1)}
Z={(0,0,1):F(1)}

def add(a,b):
    out=defaultdict(F,a)
    for m,c in b.items(): out[m]+=c
    return {m:c for m,c in out.items() if c}

def mul(a,b):
    out=defaultdict(F)
    for ma,ca in a.items():
        for mb,cb in b.items():
            out[tuple(i+j for i,j in zip(ma,mb))]+=ca*cb
    return {m:c for m,c in out.items() if c}

def scale(a,v):
    return {m:c*v for m,c in a.items() if c*v}

def evaluate(p,point):
    return sum((c*point[0]**m[0]*point[1]**m[1]*point[2]**m[2]
                for m,c in p.items()),F(0))

def ideals(p):
    for mask in range(1<<len(p)):
        if all((mask&p[i])==p[i] for i in range(len(p)) if mask>>i&1):
            yield mask

def transition(p,mask,t):
    w=bin(mask).count("1")
    m=sum(1 for i in range(len(p)) if mask>>i&1 and not any(
        (mask>>j&1) and (p[j]>>i&1) for j in range(len(p))))
    result=ZERO
    for k in range(m,w+1):
        result=add(result,scale(t[k],comb(w-m,k-m)))
    return result

def density(p,k):
    total=sum(all((p[j]>>i)&1 for i,j in combinations(S,2))
              for S in combinations(range(len(p)),k))
    return F(total,comb(len(p),k))

states={():ONE}
for n in range(4):
    nxt={}
    for p,mass in states.items():
        for mask in ideals(p):
            q=p+(mask,)
            nxt[q]=add(nxt.get(q,ZERO),
                       mul(mass,transition(p,mask,(ONE,X,Y,Z))))
    states=nxt
    assert len(states)==(1,2,7,40)[n]

numer=[[ZERO,ZERO] for _ in range(3)]
denom=[ZERO,ZERO]
terminal=set()
for p,mass in states.items():
    for mask in ideals(p):
        q=p+(mask,)
        terminal.add(q)
        weights=(transition(p,mask,(ONE,X,Y,Z,ZERO)),
                 ONE if mask==15 else ZERO)
        for j,weight in enumerate(weights):
            contribution=mul(mass,weight)
            denom[j]=add(denom[j],contribution)
            for i,k in enumerate((2,3,4)):
                numer[i][j]=add(numer[i][j],
                                scale(contribution,density(q,k)))
assert len(terminal)==357

polynomials=[*denom,*(p for row in numer for p in row)]
assert all(all(c>=0 for c in p.values()) for p in polynomials)
assert all(denom) and F(1) in denom[1].values()

center=(F(684064,100000000),F(222049,10000000),
        F(17390282,100000000))
radius=F(1,100000)
lower=tuple(c-radius for c in center)
upper=tuple(c+radius for c in center)
assert all(x>0 for x in lower)
thresholds=(F(19,100),F(1,50),F(7,10000))
targets=(F(1,10),F(1,350),F(1,29400))
for i,k in enumerate((2,3,4)):
    gap0=evaluate(numer[i][0],lower)-thresholds[i]*evaluate(denom[0],upper)
    gap1=evaluate(numer[i][1],lower)-thresholds[i]*evaluate(denom[1],upper)
    assert gap0>0 and gap1>0 and thresholds[i]>targets[i]
    print(f"CHAIN_{k}_CONSTANT_GAP := {gap0}")
    print(f"CHAIN_{k}_T4_GAP := {gap1}")
print("N4_STATES := 40")
print("N5_STATES := 357")
print("SYMBOLIC_ALL_COEFFICIENTS_NONNEGATIVE := PASS")
print("UNIFORM_FIVE_EVENT_BOX_NONEXTENSION := COMPUTATION_PASS")
print("GLOBAL_FOUR_EVENT_UNIQUENESS := NOT_REPLAYED")
print("LEAN_VERIFIED := NO")
print("NOVELTY := OPEN")
