#!/usr/bin/env python3
"""Exact finite probabilities for two disjoint-chain poset families matching
Minkowski fixed-j predecessor-count constants, yet p_(N,2) tends to 0 vs 1.
The asymptotic construction is analytical; script verifies exact finite fixtures.
No statement that either family is a realizable Minkowski sprinkling.
"""
from math import sqrt, pi, isqrt, floor
from fractions import Fraction as Q

def build(k):
    N=k*k
    J=isqrt(k)
    c=3*sqrt(pi)
    t=[]
    for j in range(J+1):
        t.append(floor(c*k))
        c*=Q(2*j+1, 2*j+2)
    assert t==sorted(t,reverse=True) and t[-1]>0
    lengths=[]
    for j in range(J):
        lengths.extend([j+1]*(t[j]-t[j+1]))
    lengths.extend([J+1]*t[J])
    base=sum(lengths)
    assert len(lengths)==t[0]
    assert base<N,(k,base,N)
    extra=N-base
    long=list(lengths)
    # last T_J chains have length J+1, so exactly one gets extra.
    long[-1]+=extra
    balanced=list(lengths)
    q,r=divmod(extra,t[J])
    for i in range(t[J]):
        balanced[-1-i]+=q+int(i<r)
    assert sum(long)==sum(balanced)==N
    assert all(sum(ell>j for ell in z)==t[j] for z in (long,balanced) for j in range(J+1))
    return N,J,t,long,balanced,base

def stats(lengths):
    N=sum(lengths)
    qmax=Q(max(lengths),N)
    p2=Q(sum(ell*(ell-1) for ell in lengths), N*(N-1))
    S=Q(sum(ell*ell for ell in lengths),N*N)
    assert p2<=S<=qmax
    return qmax,p2,S

for k in (40,80,160,320,640,1280):
    N,J,t,A,B,base=build(k)
    qa,pa,sa=stats(A); qb,pb,sb=stats(B)
    print('k=',k,'N=',N,'J=',J,'base=',base,
          'H0=',t[0],'H1=',t[1], 'H_J=',t[-1])
    print(' concentration: qmax=',format(float(qa),'.8f'),
          'p2=',format(float(pa),'.8f'))
    print(' balanced:      qmax=',format(float(qb),'.8f'),
          'p2=',format(float(pb),'.8f'))
    assert pa>pb and qa>qb
print('IDENTICAL_FIXED_J_COUNTS_FOR_EACH_PAIR := PASS')
print('EXACT_FIRST_TWO_PROBABILITIES := PASS')
print('ASYMPTOTIC_ANALYTICAL_LIMITS := concentrated -> 1, balanced -> 0')
print('MINKOWSKI_REACHABILITY := NOT_ESTABLISHED')
print('LEAN_VERIFIED := NOT_RUN')
