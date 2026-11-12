#!/usr/bin/env python3
"""Bounded reproducible exact extension-weighted prefix statistics on Minkowski sprinklings.
Python stdlib only, read-only, seed fixed, finite evidence ONLY, no asymptotic inference.
"""
import random, math
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
SEED=20261112
rng=random.Random(SEED)

def point():
    u=rng.random()
    t=(u/8)**.25 if u<.5 else 1-((1-u)/8)**.25
    r=min(t,1-t)*rng.random()**(1/3)
    xyz=[rng.gauss(0,1) for _ in range(3)]; norm=math.sqrt(sum(x*x for x in xyz))
    return (t,*(r*x/norm for x in xyz))

def predecessors(pts):
    pred=[]
    for i,(t,*x) in enumerate(pts):
        mask=0
        for j,(s,*y) in enumerate(pts):
            if s<t and (t-s)**2>sum((a-b)**2 for a,b in zip(x,y)):
                mask|=1<<j
        pred.append(mask)
    return pred

def pair_stats(pred):
    N=len(pred); full=(1<<N)-1
    @lru_cache(None)
    def ext(mask):
        if not mask:return 1
        return sum(ext(mask^(1<<v)) for v in range(N)
                   if mask>>v&1 and pred[v]&mask==0)
    den=ext(full)
    full_pairs=sum(bool(pred[a]>>b&1 or pred[b]>>a&1) for a,b in combinations(range(N),2))
    total=0
    for a,b in combinations(range(N),2):
        I=(1<<a)|(1<<b)
        if pred[a]&~I or pred[b]&~I:continue
        if pred[a]>>b&1 or pred[b]>>a&1:
            total+=ext(I)*ext(full^I)
    return Fraction(total,den),Fraction(full_pairs,math.comb(N,2)),ext.cache_info().currsize

print('SEED :=',SEED)
for N,trials in [(6,500),(8,400),(10,250),(12,150),(14,100)]:
    a=b=0; states=0
    for _ in range(trials):
        q,f,s=pair_stats(predecessors([point() for _ in range(N)]))
        a+=float(q);b+=float(f);states+=s
    print('N=',N,'trials=',trials,'prefix2_mean=',round(a/trials,6),'full2_mean=',round(b/trials,6),'avg_DP_states=',round(states/trials,1))
print('ASYMPTOTIC_MINKOWSKI_DOUBLE_LIMIT := OPEN')
