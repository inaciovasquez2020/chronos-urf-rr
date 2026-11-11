#!/usr/bin/env python3
"""Exact independent finite causal-set audit, standard library only.
Uniform natural extensions of three six-point posets; no Git operations.
"""
from itertools import permutations, combinations
from collections import Counter
from fractions import Fraction as F

cases = [
    ('antichain', (0,0,0,0,0,0), F(37,70)),
    ('branching', (0,0,1,2,5,10), F(1,35)),
    ('three_disjoint_edges', (0,0,0,1,2,4), F(31,70)),
]

def f(rows):
    n=len(rows)
    p=sum(a.bit_count() for a in rows)
    t=sum(bool(rows[j]>>i&1 and rows[k]>>j&1) for i,j,k in combinations(range(n),3))
    z=0
    for sub in combinations(range(n),4):
        ed=[(i,j) for i,j in combinations(sub,2) if rows[j]>>i&1]
        z+=len(ed)==2 and len({v for edge in ed for v in edge})==4
    return (F(p,n*(n-1)//2) if n>1 else None,
            F(t,n*(n-1)*(n-2)//6) if n>2 else None,
            F(z,n*(n-1)*(n-2)*(n-3)//24) if n>3 else None)

def linear_extensions(rows):
    n=len(rows)
    for order in permutations(range(n)):
        seen=0
        for v in order:
            if rows[v]&~seen: break
            seen |= 1<<v
        else:yield order

def induced(rows,order,n):
    ids=order[:n]
    return tuple(sum(1<<i for i,u in enumerate(ids[:j]) if rows[v]>>u&1) for j,v in enumerate(ids))

measure={n:Counter() for n in range(1,7)}
for name,rows,mass in cases:
    exts=list(linear_extensions(rows)); assert exts
    print('CLASS',name,'mass',mass,'linear_extensions',len(exts))
    avg={n:[F(0),F(0),F(0)] for n in range(2,7)}
    for order in exts:
        for n in range(1,7):
            sub=induced(rows,order,n)
            measure[n][sub]+=mass/F(len(exts))
            if n>=2:
                val=f(sub)
                for k in range(3):
                    if val[k] is not None:avg[n][k]+=val[k]/len(exts)
    for n in range(2,7):print(' CLASS_MOMENTS',name,'N',n,*(str(x) for x in avg[n]))
for n in range(1,7):
    assert sum(measure[n].values())==1
    p2=sum((w*f(r)[0] for r,w in measure[n].items() if n>=2),F(0)) if n>=2 else None
    p3=sum((w*f(r)[1] for r,w in measure[n].items() if n>=3),F(0)) if n>=3 else None
    p22=sum((w*f(r)[2] for r,w in measure[n].items() if n>=4),F(0)) if n>=4 else None
    print('TOTAL',n,len(measure[n]),p2,p3,p22)
    if n in (4,5,6):
        assert p2==F(1,10),(n,'p2')
        assert p3==F(1,350),(n,'p3')
        assert p22==F(37,350),(n,'p22')
    if n<6:
        for r,w in measure[n].items():
            assert sum((v for rr,v in measure[n+1].items() if rr[:n]==r),F(0))==w,(n,r)
# Every diamond/square of positive states is path independent by telescoping.
# Test it by enumerating all incomparable pair extensions of each supported prefix.
square_count=0
for n in range(1,5):
    for r,w in measure[n].items():
        if not w:continue
        for rxy,t in measure[n+2].items():
            if not t or rxy[:n]!=r or (rxy[-1]>>(n)&1):continue
            # swap the last two, retaining a valid natural labeled order
            r_yx = rxy[:n]+(rxy[-1]&((1<<n)-1), rxy[-2])
            if r_yx not in measure[n+2] or not measure[n+2][r_yx]:continue
            # two distinct intermediate states; test exact cross-product of path ratios
            first=rxy[:n+1]
            other=r_yx[:n+1]
            assert (measure[n+1][first]/w)*(t/measure[n+1][first]) == (measure[n+1][other]/w)*(measure[n+2][r_yx]/measure[n+1][other])
            square_count+=1
print('POSITIVE_COVARIANCE_SQUARES',square_count)
print('FINITE_4_TO_6_TARGET_MATCH := PASS')
print('FULL_INFINITE_EMERGENCE := OPEN')