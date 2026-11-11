#!/usr/bin/env python3
"""Read-only exact conditional prefix-ideal DP for finite Minkowski sprinkles."""
from __future__ import annotations
import math, random, statistics, time
from functools import lru_cache
from itertools import permutations

SEED=20261111
SIZES=[(8,80),(12,80),(16,70)]
MAX_IDEALS=150000
MAX_SECONDS=35

def sprinkle(n,rng):
    points=[]
    for _ in range(n):
        a=1-rng.random()**0.25
        t=a*(1 if rng.random()<.5 else -1)
        r=(1-a)*rng.random()**(1/3)
        g=[rng.gauss(0,1) for _ in range(3)]
        v=math.sqrt(sum(z*z for z in g))
        points.append((t,*(r*z/v for z in g)))
    points.sort()
    predecessors=[]
    for j,y in enumerate(points):
        s=0
        for i,x in enumerate(points[:j]):
            dt=y[0]-x[0]
            if dt*dt>sum((y[q]-x[q])**2 for q in range(1,4)):
                s|=1<<i
        predecessors.append(s)
    return predecessors

def prefix_means(pred,cap=MAX_IDEALS):
    n=len(pred); top=(1<<n)-1
    @lru_cache(None)
    def E(mask):
        if E.cache_info().currsize>cap:raise RuntimeError('INCOMPLETE_RESOURCE_GUARD')
        if mask==top:return 1
        return sum(E(mask|1<<j) for j in range(n) if not(mask>>j&1) and not(pred[j]&~mask))
    total=E(0)
    # F(mask) counts natural prefix paths ending at ideal mask.
    F={0:1}
    pair_num=[0]*(n+1)
    tri_num=[0]*(n+1)
    def relations(mask):
        return sum((pred[j]&mask).bit_count() for j in range(n) if mask>>j&1)
    def three(mask):
        return sum((pred[k]&mask).bit_count() for j in range(n) if mask>>j&1
                   for k in range(j) if mask>>k&1 and pred[j]>>k&1)
    for size in range(n+1):
        nxt={}
        for mask,count in F.items():
            weight=count*E(mask)
            pair_num[size]+=weight*relations(mask)
            tri_num[size]+=weight*three(mask)
            if size<n:
                for j in range(n):
                    if not (mask>>j&1) and not(pred[j]&~mask):
                        nm=mask|1<<j
                        nxt[nm]=nxt.get(nm,0)+count
        if size<n:F=nxt
    pair=[pair_num[k]/(total*math.comb(k,2)) if k>=2 else None for k in range(n+1)]
    tri=[tri_num[k]/(total*math.comb(k,3)) if k>=3 else None for k in range(n+1)]
    return pair,tri,E.cache_info().currsize

def brute(pred):
    n=len(pred)
    orders=[]
    for z in permutations(range(n)):
        seen=0;ok=True
        for v in z:
            if pred[v]&~seen:ok=False;break
            seen|=1<<v
        if ok:orders.append(z)
    out=[]
    for k in range(2,n+1):
        out.append(sum(sum(bool(pred[z[j]]>>z[i]&1) for j in range(k) for i in range(j)) for z in orders)/(len(orders)*math.comb(k,2)))
    return out

for pred in ([0,1,1], [0,1,0,0], [0,0,3,0], [0,1,1,0,0]):
    a,_,_=prefix_means(pred)
    b=brute(pred)
    assert all(abs(a[k]-b[k-2])<1e-13 for k in range(2,len(pred)+1))
print('BRUTE_FORCE_VS_EXACT_IDEAL_DP := PASS',flush=True)

start=time.monotonic();rng=random.Random(SEED)
for n,reps in SIZES:
    data=[]
    for i in range(reps):
        if time.monotonic()-start>MAX_SECONDS:
            print('INCOMPLETE_TIMEOUT',n,i,flush=True);break
        try:
            pair,tri,states=prefix_means(sprinkle(n,rng))
        except RuntimeError:
            print('INCOMPLETE_RESOURCE_GUARD',n,i,flush=True);break
        data.append((pair,tri,states))
    if len(data)!=reps:
        print('INCOMPLETE',n,len(data),'of',reps,flush=True);break
    print('N',n,'REPS',reps,'MAX_STATES',max(d[2] for d in data),flush=True)
    for k in sorted({2,3,n//2,n-2,n}):
        if k<2:continue
        pair=[d[0][k] for d in data]
        tri=[d[1][k] for d in data] if k>=3 else []
        gap=[d[0][k]-d[0][n] for d in data]
        se=statistics.stdev(gap)/math.sqrt(reps) if reps>1 else float('nan')
        print('  PREFIX',k,'PAIR',round(statistics.mean(pair),7),'PAIR_MINUS_FULL',round(statistics.mean(gap),7),'SE',round(se,7),'TRI',round(statistics.mean(tri),7) if tri else '-',flush=True)
print('ELAPSED',round(time.monotonic()-start,2),flush=True)