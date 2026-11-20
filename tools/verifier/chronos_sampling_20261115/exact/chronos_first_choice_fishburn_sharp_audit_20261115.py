#!/usr/bin/env python3
"""Exact regression of sharp first-choice collision bound for all labeled 4-posets.
Published Fishburn inequality is an external theorem; these finite checks do not prove it.
No inference about Minkowski sampling convergence.
"""
from itertools import combinations,product
from functools import lru_cache
from fractions import Fraction as Q
from math import comb

checks=0; eq=0; strict=0
for states in product(range(3),repeat=6):
    E=set()
    for (a,b),st in zip(combinations(range(4),2),states):
        if st==1:E.add((a,b))
        if st==2:E.add((b,a))
    if any((a,c) not in E for a,b in E for bb,c in E if b==bb):continue
    pred=[sum(1<<a for a,b in E if b==i) for i in range(4)]
    @lru_cache(None)
    def e(mask):
        if mask==15:return 1
        return sum(e(mask|(1<<v)) for v in range(4) if not (mask&(1<<v)) and not(pred[v]&~mask))
    q={x:Q(e(1<<x),e(0)) for x in range(4) if not pred[x]}
    C=sum((v*v for v in q.values()),Q())
    p=Q(sum(e((1<<x)|(1<<y)) for x in q for y in range(4) if pred[y]==(1<<x)),e(0))
    bound=(4*C-1)/3
    assert p<=bound,(E,p,bound)
    checks+=1;eq+=(p==bound);strict+=(p<bound)
assert checks==219
for m in range(2,12):
    for L in range(1,30):
        N=m*L
        C=Q(1,m)
        p=Q(L-1,N-1)
        assert p==(N*C-1)/(N-1)
print('FOUR_LABELED_POSETS :=',checks)
print('SHARP_FISHBURN_BOUND := PASS')
print('EQUALITIES :=',eq,'STRICT :=',strict)
print('DISJOINT_EQUAL_CHAINS_EQUALITY := PASS')
print('INFINITE_MINKOWSKI_COLLISION_LIMIT := OPEN')
