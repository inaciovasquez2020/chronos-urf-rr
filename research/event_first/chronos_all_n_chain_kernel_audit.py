#!/usr/bin/env python3
"""Exact finite checks of the all-N Chinese-restaurant disjoint-chain causal growth kernel.
No dependencies. No repository mutation. Conjectural spacetime emergence NOT claimed.
"""
from fractions import Fraction as F
from collections import defaultdict
from itertools import combinations

def evolve(dist, theta):
    out=defaultdict(F)
    for state,prob in dist.items():
        # State is tuple of chains, each chain tuple of natural birth labels.
        n=sum(map(len,state)); denom=theta+n
        out[state+((n,),)] += prob*theta/denom
        for i,ch in enumerate(state):
            new=state[:i]+(ch+(n,),)+state[i+1:]
            out[new] += prob*F(len(ch),1)/denom
    return dict(out)

def order_moments(state):
    n=sum(map(len,state))
    if n<2: return None
    pair=sum(len(c)*(len(c)-1)//2 for c in state)
    triple=sum(len(c)*(len(c)-1)*(len(c)-2)//6 for c in state)
    two2=sum((len(a)*(len(a)-1)//2)*(len(b)*(len(b)-1)//2)
             for a,b in combinations(state,2))
    return F(pair,n*(n-1)//2), (F(triple,n*(n-1)*(n-2)//6) if n>=3 else None), (F(two2,n*(n-1)*(n-2)*(n-3)//24) if n>=4 else None)

def verify(theta,max_n=7):
    dist={():F(1)}
    stats={}
    for n in range(1,max_n+1):
        dist=evolve(dist,theta)
        assert sum(dist.values())==1,(n,'normalization')
        assert len(dist)==[1,2,5,15,52,203,877][n-1],(n,len(dist))
        if n>=2:
            p2=sum(v*order_moments(s)[0] for s,v in dist.items())
            assert p2==F(1,1+theta)
            p3=(sum(v*order_moments(s)[1] for s,v in dist.items()) if n>=3 else None)
            p22=(sum(v*order_moments(s)[2] for s,v in dist.items()) if n>=4 else None)
            if n>=3: assert p3==F(2,(theta+1)*(theta+2))
            if n>=4: assert p22==F(3*theta,(theta+1)*(theta+2)*(theta+3))
            stats[n]=(p2,p3,p22)
    return stats

def main():
    for theta in [F(1),F(3,2),F(9)]:
        stats=verify(theta)
        print('THETA',theta, 'N=7 EXACT',(stats[7]))
        print('ANALYTIC',F(1,1+theta),F(2,(theta+1)*(theta+2)),F(3*theta,(theta+1)*(theta+2)*(theta+3)))
    p2=F(1,10); p3=F(1,350)
    theta=1/p2-1
    actual=F(2,(theta+1)*(theta+2))
    assert theta==9 and actual==F(1,55) and actual>p3
    assert F(1,100)>p3
    print('MINKOWSKI_PAIR_MATCH := theta=9')
    print('CHAIN_TARGET := 1/350; CHAIN_MODEL :=',actual)
    print('UNIVERSAL_CHAIN_PARTITION_LOWER_BOUND := P3 >= P2^2 = 1/100')
    print('NORMALIZATION_PREFIX_MOMENTS_N_LE_7 := PASS')
    print('LEAN_VERIFIED := NOT_RUN')
if __name__=='__main__': main()