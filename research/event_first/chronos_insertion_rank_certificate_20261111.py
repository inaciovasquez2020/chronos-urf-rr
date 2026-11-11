#!/usr/bin/env python3
"""Exact finite-poset insertion-rank and successor dominance certificates.

Read-only; Python standard library; exhaustive forward-edge closures to 5 vertices.
These tests do not establish any Minkowski N->infinity limit.
"""
from itertools import combinations
from fractions import Fraction
from math import comb


def closure(n, bits):
    p = [0]*n
    idx = 0
    for y in range(n):
        for x in range(y):
            if (bits >> idx) & 1: p[y] |= 1 << x
            idx += 1
    for y in range(n):
        for x in range(y):
            if (p[y] >> x) & 1: p[y] |= p[x]
    return tuple(p)


def extensions(p):
    n=len(p)
    def walk(prefix, seen):
        if len(prefix)==n:
            yield prefix
            return
        for x in range(n):
            if not (seen >> x)&1 and not (p[x] & ~seen):
                yield from walk(prefix+(x,),seen|(1<<x))
    yield from walk((),0)


def insertion_probabilities(p,x):
    n=len(p)
    others=tuple(y for y in range(n) if y!=x)
    strict_future=frozenset(y for y in others if (p[y]>>x)&1)
    strict_past=frozenset(y for y in others if (p[x]>>y)&1)
    # Build explicit linear extensions of P \ {x}, independently from P.
    sub = []
    def walk(seq, seen):
        if len(seq)==n-1:
            sub.append(seq); return
        for y in others:
            if not ((seen>>y)&1) and not (p[y] & ~seen & ~(1<<x)):
                walk(seq+(y,),seen|(1<<y))
    walk((),0)
    numerator=[0]*(n+1)
    total=0
    for tau in sub:
        rank={y:i+1 for i,y in enumerate(tau)}
        A=max((rank[y] for y in strict_past),default=0)
        B=min((rank[y] for y in strict_future),default=n)
        assert A<B,(p,x,tau,A,B)
        total += B-A
        for cutoff in range(1,n+1):
            numerator[cutoff] += max(0,min(cutoff,B)-A)
    assert total
    return [Fraction(t,total) for t in numerator], Fraction(numerator[1],total), len(sub), total


def verify(p):
    n=len(p)
    all_ext=list(extensions(p)); E=len(all_ext)
    weights={}
    for x in range(n):
        q,pfirst,subext,total=insertion_probabilities(p,x)
        assert total==E
        for cutoff in range(1,n+1):
            expected=Fraction(sum(x in e[:cutoff] for e in all_ext),E)
            assert q[cutoff]==expected,(p,x,cutoff,q[cutoff],expected)
        assert pfirst==Fraction(sum(e[0]==x for e in all_ext),E) if p[x]==0 else pfirst==0
        if p[x]==0:
            future=sum(bool(p[y]>>x&1) for y in range(n))
            assert pfirst >= Fraction(1,n-future),(p,x,pfirst,n-future)
        weights[x]=q
    # Future-set dominance among minimal elements implies first-step and rank inclusion dominance.
    for x in range(n):
        if p[x]:continue
        for y in range(n):
            if x==y or p[y]:continue
            upx={z for z in range(n) if (p[z]>>x)&1}
            upy={z for z in range(n) if (p[z]>>y)&1}
            if upy.issubset(upx):
                for cutoff in range(1,n+1):
                    assert weights[x][cutoff]>=weights[y][cutoff],(p,x,y,cutoff)
    return n*(n+1)//2


def main():
    configurations=0
    marginal_checks=0
    for n in range(2,6):
        for bits in range(1<<comb(n,2)):
            p=closure(n,bits)
            marginal_checks+=verify(p)
            configurations+=1
    print('EXHAUSTIVE_FORWARD_EDGE_CONFIGURATIONS :=',configurations)
    print('EXACT_EVENT_PREFIX_MARGINAL_CHECKS :=',marginal_checks)
    print('INSERTION_INTERVAL_FORMULA := PASS')
    print('MINIMAL_FIRST_LOWER_BOUND := PASS')
    print('FUTURE_SET_DOMINANCE := PASS')
    print('MINKOWSKI_LINEAR_EXTENSION_ASYMPTOTICS := OPEN')


if __name__=='__main__':main()
