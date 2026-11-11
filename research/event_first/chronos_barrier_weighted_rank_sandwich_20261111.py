#!/usr/bin/env python3
"""Exact weighted internal-order barrier sandwich; exhaustive n<=5.
Corrects an INVALID shortcut using only external predecessor cardinality.
Standard library, deterministic, no repository mutation.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import comb

def closure(n,edges):
    p=[0]*n; b=0
    for y in range(n):
        for x in range(y):
            if edges>>b&1:p[y]|=1<<x
            b+=1
    for y in range(n):
        for x in range(y):
            if p[y]>>x&1:p[y]|=p[x]
    return tuple(p)

def linear_exts(p, vertices):
    vertices=tuple(sorted(vertices));submask=sum(1<<v for v in vertices)
    def go(seq,seen):
        if len(seq)==len(vertices):yield seq;return
        for v in vertices:
            if not (seen>>v&1) and not (p[v]&submask&~seen):
                yield from go(seq+(v,),seen|1<<v)
    yield from go((),0)

def barrier_weights(a, c):
    u=len(c)
    @lru_cache(None)
    def W(i,j):
        if i==a and j==u:return 1
        return (W(i+1,j) if i<a else 0)+(W(i,j+1) if j<u and i>=c[j] else 0)
    den=W(0,0)
    numerator=sum((d+1)*W(d,1) for d in range(c[0],a+1))
    assert numerator>=den and den>0
    return den,numerator

def check(p):
    N=len(p);tested=0;refuted_count_based=0;strict_gap=0
    for x in range(N):
        if p[x]:continue
        U={y for y in range(N) if p[y]>>x&1}
        if not U:continue
        A={y for y in range(N) if y!=x and y not in U}
        u=len(U);a=len(A)
        total=0; totalB=0; low=0; high=0
        for alpha in linear_exts(p,A):
            rank={z:i+1 for i,z in enumerate(alpha)}
            for beta in linear_exts(p,U):
                c=[]
                for y in beta:
                    c.append(max(c[-1] if c else 0, max((rank[z] for z in A if p[y]>>z&1),default=0)))
                assert tuple(c)==tuple(sorted(c))
                weight,bnum=barrier_weights(a,c)
                total+=weight;totalB+=bnum
                low+=weight*F(N+c[0]*u,u+1)
                high+=weight*F(N+c[-1]*u,u+1)
        EB=F(totalB,total)
        lower=F(low,total);upper=F(high,total)
        assert lower<=EB<=upper,(p,x,lower,EB,upper)
        actual=list(linear_exts(p,range(N)))
        first=sum(t[0]==x for t in actual)
        assert F(first,len(actual))==1/EB
        R=sum(any(p[y]>>z&1 for y in U) for z in A)
        fake=F(N+R*u,u+1)
        refuted_count_based+=EB>fake
        strict_gap+=lower<upper
        tested+=1
    return tested,refuted_count_based,strict_gap

def main():
    total=[0,0,0]
    for n in range(2,6):
        counts=[0,0,0]
        for edges in range(1<<comb(n,2)):
            v=check(closure(n,edges));counts=[a+b for a,b in zip(counts,v)]
        total=[a+b for a,b in zip(total,counts)]
        print('N=',n,'checked/naive_counterexamples/strict_sandwich=',counts,flush=True)
    print('TOTAL=',total)
    print('WEIGHTED_BARRIER_RANK_SANDWICH := PASS')
    print('COUNT_BASED_UPPER_BOUND := REFUTED')
    print('GEOMETRIC_WEIGHTED_BARRIER_LIMIT := OPEN')
if __name__=='__main__':main()
