#!/usr/bin/env python3
"""Exact barrier monotonicity / penalty certificate. Python stdlib only.
Reproduce with python3 chronos_barrier_monotonicity_audit_20261111.py
No repository mutations, no network, no random tests; N<=6, a,u<=5.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
from fractions import Fraction as F
from math import comb

def survival(a,c):
    u=len(c)
    @lru_cache(None)
    def W(i,j):
        if i==a and j==u:return 1
        return (W(i+1,j) if i<a else 0) + (W(i,j+1) if j<u and i>=c[j] else 0)
    counts=[W(d,1) if d>=c[0] else 0 for d in range(a+1)]
    den=sum(counts)
    assert den==W(0,0)>0
    # B=d+1, B>j iff d>=j
    return tuple(F(sum(counts[j:]),den) for j in range(a+2))

def check_barriers():
    checked=0
    for a in range(1,6):
      for u in range(1,6):
        C=list(combinations_with_replacement(range(a+1),u))
        S={c:survival(a,c) for c in C}
        for c in C:
          for d in C:
            if not all(ci<=di for ci,di in zip(c,d)):continue
            assert all(t<=z for t,z in zip(S[c],S[d])),(a,u,c,d,S[c],S[d])
            checked+=1
    return checked

def closure(n,edge_bits):
    pred=[0]*n;k=0
    for j in range(n):
      for i in range(j):
        if edge_bits>>k&1: pred[j]|=1<<i
        k+=1
    for j in range(n):
      for i in range(j):
        if pred[j]>>i&1:pred[j]|=pred[i]
    return tuple(pred)

def check_poset(n,bits):
    pred=closure(n,bits);full=(1<<n)-1
    @lru_cache(None)
    def E(mask):
        if mask==full:return 1
        return sum(E(mask|1<<j) for j in range(n) if not(mask>>j&1) and pred[j]&~mask==0)
    den=E(0);checked=0;strict=0
    for x in range(n):
        if pred[x]:continue
        U={y for y in range(n) if pred[y]>>x&1};u=len(U)
        if not u:continue
        A={y for y in range(n) if y!=x and y not in U};a=len(A)
        MinU={y for y in U if not any(pred[y]>>z&1 for z in U)}
        r=min(sum(bool(pred[y]>>z&1) for z in A) for y in MinU)
        # Independent full-extension prefix enumeration of Q=P\{x} for tail bound.
        others=(1<<n)-1-(1<<x)
        @lru_cache(None)
        def Qe(mask):
            if mask==others:return 1
            return sum(Qe(mask|1<<y) for y in range(n)
                       if (others>>y&1) and not(mask>>y&1)
                       and (pred[y]&others&~mask)==0)
        qden=Qe(0)
        frontier={0:1}
        for j in range(n):
            if j:
                nxt={}
                for mask,cnt in frontier.items():
                    for y in range(n):
                        if (others>>y&1) and not(mask>>y&1) and (pred[y]&others&~mask)==0:
                            nxt[mask|1<<y]=nxt.get(mask|1<<y,0)+cnt
                frontier=nxt
            s_j=F(sum(cnt*Qe(mask) for mask,cnt in frontier.items()
                        if not any(mask>>y&1 for y in U)),qden)
            ref=(F(1) if j<=r else F(comb(a-r,j-r),comb(a-r+u,j-r)) if j<=a else F(0))
            assert s_j>=ref,(n,bits,x,j,s_j,ref)
        EB=F(den,E(1<<x))
        delta=EB-F(n,u+1)
        bound=F(r*u,u+1)
        assert delta>=bound,(n,bits,x,delta,bound)
        checked+=1
        strict+=delta>bound
    return checked,strict

def main():
    b=check_barriers()
    print('ORDERED_BARRIER_PAIRS :=',b,flush=True)
    cases=0;strict=0
    for n in range(2,7):
        for bits in range(1<<comb(n,2)):
            c,s=check_poset(n,bits)
            cases+=c;strict+=s
        print('COMPLETED_N :=',n,flush=True)
    print('FINITE_POSET_PENALTY_BOUND_CHECKS :=',cases)
    print('STRICT_SLACK_CASES :=',strict)
    print('BARRIER_MONOTONICITY := PASS')
    print('STRONGER_EXTERNAL_PREDECESSOR_BOUND := PASS')
    print('MINKOWSKI_BARIER_LIMIT := OPEN')
if __name__=='__main__':main()
