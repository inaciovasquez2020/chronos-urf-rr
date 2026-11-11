#!/usr/bin/env python3
"""Read-only exact linear-extension and uniform-subset audit. Python >=3.9, stdlib only."""
import math, random, statistics, hashlib
from functools import lru_cache
SEED=20261111
CONFIG=((8,240),(12,240),(16,240))

def sprinkle(n, rng):
    out=[]
    for _ in range(n):
        a=1-rng.random()**0.25
        t=a if rng.random()<.5 else -a
        r=(1-a)*rng.random()**(1/3)
        g=[rng.gauss(0,1) for j in range(3)]
        z=math.sqrt(sum(x*x for x in g))
        out.append((t,*(r*x/z for x in g)))
    return sorted(out)

def pred_masks(pts):
    p=[0]*len(pts)
    for j in range(len(pts)):
        for i in range(j):
            dt=pts[j][0]-pts[i][0]
            if dt>0 and dt*dt >sum((pts[j][k]-pts[i][k])**2 for k in (1,2,3)):
                p[j]|=1<<i
    return p

def exact(p):
    N=len(p); full=(1<<N)-1
    @lru_cache(maxsize=None)
    def ext(m):
        if m==full:return 1
        return sum(ext(m | (1<<j)) for j in range(N) if not (m>>j&1) and p[j]&~m==0)
    tot=ext(0)
    firstpair=firsttriple=0
    for i in range(N):
        a=1<<i
        if p[i]:continue
        for j in range(N):
            b=a|1<<j
            if a>>j&1 or (p[j]&~a):continue
            w=ext(b)
            if p[j]>>i&1:firstpair+=w
            for k in range(N):
                if b>>k&1 or (p[k]&~b):continue
                if (p[j]>>i&1) and (p[k]>>j&1):firsttriple+=ext(b|1<<k)
    fullpair=sum(int(x).bit_count() for x in p)/math.comb(N,2)
    fulltriple=sum(1 for k in range(N) for j in range(k) for i in range(j)
                  if (p[j]>>i&1) and (p[k]>>j&1))/math.comb(N,3)
    return (firstpair/tot, firsttriple/tot, fullpair, fulltriple)

def report():
    rng=random.Random(SEED)
    print('SEED',SEED,'PYTHON_STD_LIB_ONLY',True)
    print('SAMPLING: four-dimensional flat causal diamond, density proportional to (1-|t|)^3')
    for n,reps in CONFIG:
        rows=[exact(pred_masks(sprinkle(n,rng))) for _ in range(reps)]
        means=[statistics.mean(row[i] for row in rows) for i in range(4)]
        sem=[statistics.stdev(row[i] for row in rows)/math.sqrt(reps) for i in range(4)]
        diff=[row[0]-row[2] for row in rows]
        dmean=statistics.mean(diff)
        dsem=statistics.stdev(diff)/math.sqrt(reps)
        print('N',n,'reps',reps,'mean',*(f'{v:.7f}' for v in means),'SEM',*(f'{v:.7f}' for v in sem),
              'pair_prefix_minus_full',f'{dmean:.7f}','paired_SEM',f'{dsem:.7f}')
    # Exact coupling for any n-prefix P of N-poset, uniformly sampling k elements.
    # Choose k-subset U of full set; if U contained in prefix use same subset,
    # otherwise draw an independent uniform k-subset of prefix.
    # The subset of prefix conditional on containment is uniform.
    from fractions import Fraction
    for N,n,k in [(100,99,2),(100,90,2),(100,50,3),(1000,990,3)]:
        gap=1-Fraction(math.comb(n,k),math.comb(N,k))
        print('COUPLING_TV_UPPER_BOUND',N,n,k,str(gap),f'{float(gap):.8f}')
    print('RESULT := FINITE_SAMPLE_ONLY; NO_ASYMPTOTIC_CLAIM')
if __name__=='__main__':report()