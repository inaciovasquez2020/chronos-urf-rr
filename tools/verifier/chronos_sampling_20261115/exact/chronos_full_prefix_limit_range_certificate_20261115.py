#!/usr/bin/env python3
"""Exact finite rational tests of arbitrary p_(N,2) limits at fixed-j count profile.
Analytical asymptotic proof is in companion .md. Stdlib only, no writes.
"""
from fractions import Fraction as Q
from chronos_matching_all_fixed_predecessor_counts_counterexample_20261115 import build, stats

alphas = [Q(0), Q(1,4), Q(1,2), Q(3,4), Q(1)]
for k in (80,160,320,640,1280):
    N,J,M,_,_,S=build(k)
    tail=M[J]
    assert tail>=2
    for alpha in alphas:
        # use same chain length histogram through J for every alpha
        lengths=[]
        for j in range(J): lengths += [j+1]*(M[j]-M[j+1])
        lengths += [J+1]*M[J]
        extra=N-sum(lengths)
        L=int(extra*alpha)
        lengths[-1]+=L
        rest=extra-L
        q,r=divmod(rest,tail-1)
        for i in range(tail-1):
            lengths[-2-i]+=q+(i<r)
        assert sum(lengths)==N
        assert all(sum(z>j for z in lengths)==M[j] for j in range(J+1))
        _,p,_=stats(lengths)
        target=alpha*alpha
        # Not a finite-sample tolerance proof, only display convergence pattern
        print('N',N,'J',J,'alpha',str(alpha),'p2',round(float(p),9),
              'target',str(target),'absdiff',round(abs(float(p-target)),9))
print('FINITE_IDENTICAL_COUNT_PROFILE := PASS')
print('FINITE_EXACT_EXTENSION_PROBABILITIES := PASS')
print('ARBITRARY_LIMIT_THEOREM := ANALYTIC_PROOF_IN_COMPANION_NOTE')
print('MINKOWSKI_REALIZABILITY := NOT_ESTABLISHED')
