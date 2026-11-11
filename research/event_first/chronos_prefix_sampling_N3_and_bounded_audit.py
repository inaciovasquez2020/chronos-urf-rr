#!/usr/bin/env python3
"""Read-only exact N=3 prefix law + bounded diamond linear-extension experiment.
Python 3.9+ standard library. No repository changes; no dependency downloads.
Coordinate draws are floating-point; conditional extension counts are exact integers.
"""
import math, random, statistics, time, itertools
from fractions import Fraction as F
from functools import lru_cache

# Analytical ingredients for 4D flat causal diamond (these are EXACT references).
P2, P3, FORK_INC = F(1,10), F(1,350), F(1,35)
strict_fork = FORK_INC-P3
single_edge_labeled = (3*P2-3*P3-4*strict_fork)/3
antichain = 1 - P3 - 3*single_edge_labeled-2*strict_fork
prefix_pair_N3=P3+single_edge_labeled+strict_fork
assert (strict_fork,single_edge_labeled,antichain,prefix_pair_N3)==(F(9,350),F(11,175),F(53,70),F(16,175))
assert P2-prefix_pair_N3 == F(3,350)
print('EXACT_N3_DISTRIBUTION := PASS')
print('N3_CHAIN',P3,'STRICT_FORK_EACH_ORIENTATION',strict_fork,
      'SINGLE_EDGE_EACH_LABEL',single_edge_labeled,'ANTICHAIN',antichain)
print('N3_PREFIX_PAIR',prefix_pair_N3,'FULL_UNIFORM_PAIR',P2,
      'TOTAL_VARIATION_DISTANCE',P2-prefix_pair_N3)

def sprinkle(n, rng):
    pts=[]
    for _ in range(n):
        u=rng.random(); at=1-u**0.25
        t=at if rng.random()<0.5 else -at
        r=(1-at)*rng.random()**(1/3)
        g=[rng.gauss(0,1) for __ in range(3)]
        z=math.sqrt(sum(a*a for a in g))
        pts.append((t,*(r*a/z for a in g)))
    return sorted(pts)

def predecessors(pts):
    pred=[0]*len(pts)
    for j in range(len(pts)):
        for i in range(j):
            delta=pts[j][0]-pts[i][0]
            if delta>0 and delta**2>sum((pts[j][h]-pts[i][h])**2 for h in (1,2,3)):
                pred[j] |= 1<<i
    return tuple(pred)

def extension_stats(pred):
    n=len(pred);full=(1<<n)-1
    @lru_cache(maxsize=None)
    def count(mask):
        if mask == full:return 1
        return sum(count(mask | (1<<j)) for j in range(n)
                   if not(mask>>j&1) and not(pred[j]&~mask))
    tot=count(0)
    pair=tri=0
    for i in range(n):
        if pred[i]:continue
        mask1=1<<i
        for j in range(n):
            if (mask1>>j&1) or (pred[j]&~mask1): continue
            mask2=mask1 | (1<<j)
            if pred[j]>>i&1:pair+=count(mask2)
            for k in range(n):
                if (mask2>>k&1) or pred[k]&~mask2:continue
                if (pred[j]>>i&1) and (pred[k]>>j&1):tri+=count(mask2|(1<<k))
    fullpair=sum(m.bit_count() for m in pred)/math.comb(n,2)
    fulltri=sum(1 for k in range(n) for j in range(k) for i in range(j)
                if (pred[j]>>i&1) and (pred[k]>>j&1))/math.comb(n,3)
    return pair/tot,tri/tot,fullpair,fulltri

def brute(pred):
    n=len(pred);pair=tri=total=0
    for perm in itertools.permutations(range(n)):
        order=[0]*n
        for idx,v in enumerate(perm):order[v]=idx
        if any(order[i]>order[j] for j in range(n) for i in range(n) if pred[j]>>i&1):continue
        total+=1
        pair+=int(bool(pred[perm[1]]>>perm[0]&1))
        tri+=int(bool(pred[perm[1]]>>perm[0]&1) and bool(pred[perm[2]]>>perm[1]&1))
    return pair/total,tri/total

# Independent factorial-permutation cross-check of the exact integer dynamic program.
rng=random.Random(799)
for n in (3,4,5,6):
    for _ in range(8):
        p=predecessors(sprinkle(n,rng))
        dp=extension_stats(p);br=brute(p)
        assert abs(dp[0]-br[0])<1e-15 and abs(dp[1]-br[1])<1e-15
print('BRUTE_FORCE_VS_DP := PASS (32 independent small posets)')

configs=((8,240),(12,240),(16,240),(18,80))
for n,reps in configs:
    rng=random.Random(20261111 + 1009*n)
    t0=time.monotonic()
    rows=[extension_stats(predecessors(sprinkle(n,rng))) for _ in range(reps)]
    vals=[statistics.mean(x[j] for x in rows) for j in range(4)]
    gap=[x[0]-x[2] for x in rows]
    mean=statistics.mean(gap)
    se=statistics.stdev(gap)/math.sqrt(reps)
    print('N',n,'REPS',reps,'PREFIX_PAIR',format(vals[0],'.8f'),
          'PREFIX_TRIPLE',format(vals[1],'.8f'),
          'FULL_PAIR',format(vals[2],'.8f'),
          'FULL_TRIPLE',format(vals[3],'.8f'),
          'PAIRED_GAP',format(mean,'.8f'),
          'PAIRED_SE',format(se,'.8f'),
          'ELAPSED_SEC',format(time.monotonic()-t0,'.2f'),flush=True)
print('ASYMPTOTIC_STABILITY := OPEN')
print('MAC_BUILD := NOT_RUN; LEAN := NOT_RUN; REPO_WRITES := NONE')