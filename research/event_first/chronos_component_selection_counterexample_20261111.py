#!/usr/bin/env python3
"""Exact certificates for component-size selection and shallow-past nonidentifiability.
Standard library; deterministic; no network or repository mutations.
"""
from fractions import Fraction
from math import isqrt
from functools import lru_cache

def induced(n, edges):
    pred=[0]*n
    for a,b in edges:
        assert a < b
        pred[b]|=1<<a
    for b in range(n):
        for a in range(b):
            if pred[b]>>a&1:pred[b]|=pred[a]
    return pred

def exact_prefix_chain_probability(pred):
    n=len(pred); full=(1<<n)-1
    @lru_cache(None)
    def E(mask):
        if mask==full:return 1
        return sum(E(mask|1<<v) for v in range(n)
                   if not mask>>v&1 and pred[v]&~mask==0)
    denominator=E(0)
    numerator=0
    first=[Fraction(0) for _ in range(n)]
    for a in range(n):
        if pred[a]:continue
        ma=1<<a
        first[a]=Fraction(E(ma),denominator)
        for b in range(n):
            if pred[b]&~ma or ma>>b&1:continue
            if (pred[b]>>a)&1:numerator+=E(ma|1<<b)
    return Fraction(numerator,denominator),first

def disjoint_chains(lengths):
    edges=[];at=0
    for L in lengths:
        for i in range(at,at+L-1):edges.append((i,i+1))
        at+=L
    return induced(at,edges)

def predicted(lengths):
    n=sum(lengths)
    return Fraction(sum(L*(L-1) for L in lengths),n*(n-1))

def shallow(lengths,k):return sum(min(k,L) for L in lengths)

def main():
    cases=0
    for N in range(2,9):
        def parts(t,head=1):
            if not t:yield []
            for v in range(head,t+1):
                for tail in parts(t-v,v):yield [v]+tail
        for Ls in parts(N):
            observed,first=exact_prefix_chain_probability(disjoint_chains(Ls))
            assert observed==predicted(Ls),(Ls,observed,predicted(Ls))
            at=0
            for L in Ls:
                assert first[at]==Fraction(L,N),(Ls,L,first[at])
                at+=L
            cases+=1
    print('EXACT_SMALL_DISJOINT_CHAIN_PARTITIONS :=',cases,flush=True)
    for N in (100,10000,1000000):
        m=isqrt(N)
        A=[N-m]+[1]*m
        B=[N//m+int(i<N%m) for i in range(m)]
        assert sum(A)==sum(B)==N
        print('N=',N,'A_min=',len(A),'B_min=',len(B),
              'A_pair=',predicted(A),'B_pair=',predicted(B),
              'A_shallow_lt2=',shallow(A,2),'B_shallow_lt2=',shallow(B,2),flush=True)
    print('NONIDENTIFIABILITY_OF_PAIR_FROM_SQRT_SHALLOW_SCALING := PROVED')
    print('MINKOWSKI_SAMPLING_LIMIT := OPEN')
if __name__=='__main__':main()
