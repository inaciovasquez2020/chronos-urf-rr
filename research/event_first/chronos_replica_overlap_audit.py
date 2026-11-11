#!/usr/bin/env python3
"""Exact replica-overlap certificate for random linear-extension prefixes.
No external dependencies or repository mutations. Bounded n<=16 DP.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations
import random, math, statistics

MAX_STATES=100000

def extension_q(pred,n):
    N=len(pred); full=(1<<N)-1
    @lru_cache(None)
    def E(mask):
        if E.cache_info().currsize > MAX_STATES: raise RuntimeError('STATE_GUARD')
        if mask==full:return 1
        return sum(E(mask|(1<<v)) for v in range(N) if not mask>>v&1 and pred[v]&~mask==0)
    total=E(0); cur={0:1}
    for _ in range(n):
        nxt={}
        for mask,count in cur.items():
            for v in range(N):
                if not mask>>v&1 and pred[v]&~mask==0:
                    m=mask|(1<<v);nxt[m]=nxt.get(m,0)+count
        cur=nxt
    assert sum(count*E(mask) for mask,count in cur.items())==total
    count=[0]*N
    for mask,a in cur.items():
        b=a*E(mask)
        for v in range(N):
            if mask>>v&1:count[v]+=b
    return [F(t,total) for t in count],cur,total,E.cache_info().currsize

def direct_q(pred,n):
    N=len(pred);count=[0]*N; total=0
    for perm in permutations(range(N)):
        used=0;ok=True
        for v in perm:
            if pred[v]&~used:ok=False;break
            used|=1<<v
        if not ok:continue
        total+=1
        for v in perm[:n]:count[v]+=1
    return [F(x,total) for x in count],total

def verify(pred,n,bruteforce=False):
    q,weights,total,states=extension_q(pred,n);N=len(q)
    if bruteforce:
        direct,brute_total=direct_q(pred,n)
        assert q==direct and total==brute_total
    assert sum(q)==n
    for y in range(N):
        for x in range(N):
            if pred[y]>>x&1:assert q[x]>=q[y]
    unconstrained=sum(min(t,1-t) for t in q)
    fixed=2*(n-sum(sorted(q,reverse=True)[:n]))
    replica=2*sum(t*(1-t) for t in q)
    assert 2*(n-sum(t*t for t in q))==replica
    assert replica/2 <= unconstrained <=fixed<=replica
    top=set(sorted(range(N),key=lambda x:(-q[x],x))[:n])
    assert all(pred[y]&~sum(1<<x for x in top)==0 for y in top)
    return (float(unconstrained/n),float(fixed/n),float(replica/n),states)

def sprinkled(n,rng):
    pts=[]
    for _ in range(n):
        a=1-rng.random()**.25;t=a*(1 if rng.random()<.5 else -1)
        r=(1-a)*rng.random()**(1/3)
        vec=[rng.gauss(0,1) for _ in range(3)];norm=math.sqrt(sum(t*t for t in vec))
        pts.append((t,*(r*z/norm for z in vec)))
    pts.sort()
    pred=[]
    for j,y in enumerate(pts):
        mask=0
        for i,x in enumerate(pts[:j]):
            dt=y[0]-x[0]
            if dt*dt>sum((y[m]-x[m])**2 for m in (1,2,3)):
                mask|=1<<i
        pred.append(mask)
    return pred

def main():
    checked=0
    for N in range(2,6):
        for edges in range(1<<(N*(N-1)//2)):
            pred=[0]*N;bit=0
            for j in range(N):
                for i in range(j):
                    if edges>>bit&1:pred[j]|=1<<i
                    bit+=1
            for j in range(N):
                for i in range(j):
                    if pred[j]>>i&1:pred[j]|=pred[i]
            for n in range(1,N):
                verify(pred,n,bruteforce=True);checked+=1
    print('EXHAUSTIVE_EDGE_CONFIGURATIONS_THROUGH_N5 := PASS',checked,flush=True)
    rng=random.Random(20261111)
    for N,reps in [(8,60),(12,60),(16,40)]:
        n=N//2;vals=[];maxstates=0
        for i in range(reps):
            vals.append(verify(sprinkled(N,rng),n))
            maxstates=max(maxstates,vals[-1][-1])
        avg=[statistics.mean(v[k] for v in vals) for k in range(3)]
        se=[statistics.stdev(v[k] for v in vals)/math.sqrt(reps) for k in range(3)]
        print('N=%d n=%d reps=%d unconstrained=%.6f fixed=%.6f replica=%.6f se=%s maxstates=%d' %(N,n,reps,*avg,[round(x,6) for x in se],maxstates),flush=True)
    print('ASYMPTOTIC_CONCENTRATION := OPEN')

if __name__=='__main__':main()
