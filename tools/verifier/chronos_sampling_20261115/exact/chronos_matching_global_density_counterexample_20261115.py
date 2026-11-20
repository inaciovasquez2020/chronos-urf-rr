#!/usr/bin/env python3
"""Exact finite counts for two poset families with matching fixed-j predecessor
profiles and common limiting global comparable-pair fraction 1/10, but
opposite limiting uniform-linear-extension prefix comparability 0 vs 1.
Irrational target fractions are approximated using float only to select
finite integer fixture sizes; all poset statistics use exact Fraction.
No realization as a Minkowski sprinkling is asserted.
"""
from fractions import Fraction as Q
from math import comb, sqrt
from chronos_matching_all_fixed_predecessor_counts_counterexample_20261115 import build

def compare(n,k):
    N,J,M,original,balanced,S=build(k)
    # baseline chain lengths from survival histogram, independent of original branch.
    lengths=[]
    for j in range(J):lengths.extend([j+1]*(M[j]-M[j+1]))
    lengths.extend([J+1]*M[J])
    assert sum(lengths)==S
    # LOW: all baseline chains, then B1 antichain, then B2 antichain.
    # Bulk above all of the small scaffold ensures H_j=M_j for j<=J.
    B=N-S
    beta=(1-sqrt(Q(4,5)))/2
    B1=round(beta*B);B2=B-B1
    low_comp=sum(comb(l,2) for l in lengths)+S*B+B1*B2
    low_p=Q(sum(l*(l-1) for l in lengths),S*(S-1))
    # HIGH: remove one length J+1 chain, insert a macroscopic long chain C;
    # then put a bulk antichain above entire lower Q. For every j<=J, the
    # long chain replaces the removed chain in H_j.
    smaller=lengths.copy();smaller.pop()
    c=1-sqrt(Q(9,10))
    C=round(c*N)
    Qsize=sum(smaller)+C
    assert C>=J+1 and Qsize < N
    A=N-Qsize
    high_comp=sum(comb(l,2) for l in smaller)+comb(C,2)+Qsize*A
    high_p=Q(sum(l*(l-1) for l in smaller)+C*(C-1),Qsize*(Qsize-1))
    assert all(sum(l>j for l in lengths)==sum(l>j for l in smaller)+int(C>j)==M[j] for j in range(J+1))
    return J,M[0],M[1],Q(low_comp,comb(N,2)),Q(high_comp,comb(N,2)),low_p,high_p

for k in (80,160,320,640,1280):
    J,h0,h1,gl,gh,pl,ph=compare(k*k,k)
    print('N',k*k,'J',J,'H0',h0,'H1',h1,
          'global_LOW',round(float(gl),7),'global_HIGH',round(float(gh),7),
          'prefix_LOW',round(float(pl),7),'prefix_HIGH',round(float(ph),7))
    assert pl<ph
print('FIXED_J_PROFILES_IDENTICAL := PASS')
print('EXACT_FINITE_PAIR_PROBABILITIES := PASS')
print('GLOBAL_COMPARABILITY_ASYMPTOTIC := 1/10 IN BOTH FAMILIES (ANALYTIC)')
print('FIRST_TWO_PREFIX_LIMITS := 0 vs 1 (ANALYTIC)')
print('MINKOWSKI_SPRINKLING_REALIZABILITY := NOT_ESTABLISHED')
