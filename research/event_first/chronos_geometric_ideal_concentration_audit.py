#!/usr/bin/env python3
"""Read-only deterministic audit: uniform linear extensions of 4D diamond samples.
Exact integer conditional ideal weights; floating geometric sampling only.
"""
import math,random,time,statistics
from functools import lru_cache
from fractions import Fraction
SEED=20261111
SIZES=((8,100),(12,100),(16,80))
ALPHAS=(0.25,0.5,0.75)
MAX_STATES=150000
MAX_SEC=35

def sprinkle(n,rng):
    points=[]
    for _ in range(n):
        a=1-rng.random()**.25
        t=a*(1 if rng.random()<.5 else -1)
        r=(1-a)*rng.random()**(1/3)
        v=[rng.gauss(0,1) for _ in range(3)]
        norm=math.sqrt(sum(z*z for z in v))
        points.append((t,*(r*z/norm for z in v)))
    points.sort()
    preds=[]
    for j,y in enumerate(points):
        mask=0
        for i,x in enumerate(points[:j]):
            if (y[0]-x[0])**2>sum((y[q]-x[q])**2 for q in range(1,4)):
                mask|=1<<i
        preds.append(mask)
    return points,preds

def prefix_weights(pred,n):
    N=len(pred);top=(1<<N)-1
    @lru_cache(None)
    def E(mask):
        if E.cache_info().currsize>MAX_STATES:raise RuntimeError('STATE_GUARD')
        if mask==top:return 1
        return sum(E(mask|1<<j) for j in range(N) if not(mask>>j&1) and not(pred[j]&~mask))
    total=E(0)
    F={0:1}
    for _ in range(n):
        nxt={}
        for mask,c in F.items():
            for j in range(N):
                if not(mask>>j&1) and not(pred[j]&~mask):
                    new=mask|1<<j
                    nxt[new]=nxt.get(new,0)+c
        F=nxt
    assert sum(c*E(mask) for mask,c in F.items())==total
    counts=[0]*N
    for mask,c in F.items():
        w=c*E(mask)
        for j in range(N):
            if mask>>j&1: counts[j]+=w
    return [Fraction(x,total) for x in counts],len(F),E.cache_info().currsize

def test():
    rng=random.Random(SEED);start=time.monotonic()
    for N,reps in SIZES:
        for alpha in ALPHAS:
            n=round(alpha*N)
            if not (2<=n<N):continue
            vals=[]; mvals=[]; states=[]
            for iteration in range(reps):
                if time.monotonic()-start>MAX_SEC:
                    print('INCOMPLETE_TIMEOUT',N,alpha,iteration,flush=True);return
                pts,pred=sprinkle(N,rng)
                try: ranks,_,state=prefix_weights(pred,n)
                except RuntimeError:
                    print('INCOMPLETE_STATE_GUARD',N,alpha,iteration,flush=True);return
                s=(n/N)**.25
                apex=-1+2*s
                A=[j for j,x in enumerate(pts) if x[0]<apex and
                   sum(z*z for z in x[1:])<(apex-x[0])**2]
                expected=sum(1-ranks[j] if j in A else ranks[j] for j in range(N))
                vals.append(float(expected/n));mvals.append(len(A));states.append(state)
            mean=statistics.mean(vals);se=statistics.stdev(vals)/math.sqrt(reps)
            print('N',N,'n',n,'reps',reps,'mismatch_over_n',round(mean,6),
                  'SE',round(se,6),'mean_diamond_count',round(statistics.mean(mvals),3),
                  'max_states',max(states),flush=True)

# tiny exact condition check: antichain of 4 => probability each vertex in 2-prefix is 1/2
assert prefix_weights([0]*4,2)[0] == [Fraction(1,2)]*4
# total chain => first 2 fixed
assert prefix_weights([0,1,3,7],2)[0] == [Fraction(1),Fraction(1),Fraction(0),Fraction(0)]
print('SMALL_EXACT_CHECK := PASS',flush=True)
test()