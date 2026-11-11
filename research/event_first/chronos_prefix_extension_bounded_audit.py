#!/usr/bin/env python3
import math,random,statistics,time
from functools import lru_cache
from fractions import Fraction

def sprinkle(n,rng):
    pts=[]
    for _ in range(n):
        a=1-rng.random()**.25;t=a*(1 if rng.random()<.5 else -1)
        r=(1-a)*rng.random()**(1/3)
        g=[rng.gauss(0,1) for _ in range(3)];norm=math.sqrt(sum(z*z for z in g))
        pts.append((t,*(r*z/norm for z in g)))
    pts.sort()
    pred=[]
    for j,q in enumerate(pts):
        mask=0
        for i,p in enumerate(pts[:j]):
            dt=q[0]-p[0]
            if dt*dt>sum((q[d]-p[d])**2 for d in (1,2,3)):mask|=1<<i
        pred.append(mask)
    return pred

def stats(pred):
    n=len(pred); allmask=(1<<n)-1
    @lru_cache(None)
    def E(mask):
        if mask==allmask:return 1
        out=0
        for j in range(n):
            if not (mask>>j)&1 and pred[j]&~mask==0:
                out+=E(mask|(1<<j))
        return out
    total=E(0);numer=0
    for i in range(n):
        if pred[i]:continue
        a=1<<i
        for j in range(n):
            if j==i or pred[j]&~a:continue
            if (pred[j]>>i)&1:numer+=E(a|(1<<j))
    return numer/total,sum(m.bit_count() for m in pred)/math.comb(n,2),E.cache_info().currsize

print('SEED := 20261111; BOUND := N<=20; EXACT_EXTENSION_DP := YES')
for n,reps in [(8,80),(12,80),(16,80),(20,60)]:
    rng=random.Random(20261111+1009*n)
    vals=[];start=time.monotonic()
    for _ in range(reps): vals.append(stats(sprinkle(n,rng)))
    gaps=[a-b for a,b,_ in vals]
    print('N',n,'REPS',reps,'PREFIX',round(statistics.mean(x[0] for x in vals),8),'UNIFORM',round(statistics.mean(x[1] for x in vals),8),'GAP',round(statistics.mean(gaps),8),'SE',round(statistics.stdev(gaps)/math.sqrt(reps),8),'MAX_STATES',max(x[2] for x in vals),'TIME',round(time.monotonic()-start,2),flush=True)