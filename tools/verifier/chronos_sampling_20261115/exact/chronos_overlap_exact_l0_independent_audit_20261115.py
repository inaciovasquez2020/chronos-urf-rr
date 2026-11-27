#!/usr/bin/env python3
"""Exact angular ℓ=0 contribution for bipartite causality graphs via simplex gaps.
Independent geometry checks against one-edge and 3/4-event star moments.
"""
from fractions import Fraction as F
from itertools import permutations
from collections import defaultdict
from math import factorial, prod

def angular_zero_mode(n,edges):
    items=tuple((i,b) for i in range(n) for b in range(2));total=0;count=0
    degree=2*n
    fac=[factorial(i) for i in range(degree+1)]
    for order in permutations(items):
        pos={k:i for i,k in enumerate(order)}
        if any(pos[i,0]>=pos[i,1] for i in range(n)):continue
        if any(pos[i,0]>=pos[j,0] or pos[i,1]>=pos[j,1] for i,j in edges):continue
        rem=[2]*n;factors=[]
        for i,j in edges:
            if pos[i,1]<pos[j,0]:continue
            assert pos[i,0]<pos[j,0]<pos[i,1]<pos[j,1]
            rem[i]-=1;rem[j]-=1
            factors.extend([(pos[i,0],pos[j,0]),(pos[i,1],pos[j,1])])
        if any(v<0 for v in rem):raise ValueError('Degree >2; not polynomial')
        for i,v in enumerate(rem):factors.extend([(pos[i,0],pos[i,1])]*v)
        assert len(factors)==2*n
        poly={(0,)*(2*n-1):1}
        for i,j in factors:
            q=defaultdict(int)
            for ex,c in poly.items():
                for k in range(i,j):
                    e=list(ex);e[k]+=1;q[tuple(e)]+=c
            poly=q
        total+=sum(c*prod(fac[a] for a in e) for e,c in poly.items())
        count+=1
    return F(12**n *total, factorial(4*n)),count

for n,edges,wanted in [
 (2,[(0,1)],F(1,20)),
 (3,[(0,2),(1,2)],F(1,105)),
 (3,[(0,1),(0,2)],F(1,105)),
 (4,[(0,2),(0,3),(1,2),(1,3)],F(513,875875)),
]:
    result,count=angular_zero_mode(n,edges)
    print('n',n,'edges',len(edges),'nonzero_interleavings',count,'EXACT',result)
    assert result==wanted,(result,wanted)
print('INDEPENDENT_NORMALIZATIONS_AND_K22_L0 := PASS')
