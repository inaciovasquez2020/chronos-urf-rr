#!/usr/bin/env python3
"""Exact linear-extension DP for i.i.d. 4D Minkowski diamond samples, N<=20.
Finite sweep only. No conclusion about N->infinity; report all resource guards.
"""
from functools import lru_cache
from fractions import Fraction as Q
from math import comb
from statistics import mean,median
from time import perf_counter
import argparse
import numpy as np

parser=argparse.ArgumentParser();parser.add_argument('--seed',type=int,default=20261115);parser.add_argument('--maxstates',type=int,default=2_000_000);args=parser.parse_args()
rng=np.random.default_rng(args.seed)

def sample(N):
    u=rng.random((N,4));q=u[:,0]
    t=np.where(q<.5,.5*(2*q)**.25,1-.5*(2*(1-q))**.25)
    r=np.minimum(t,1-t)*np.cbrt(u[:,1]);c=2*u[:,2]-1;a=2*np.pi*u[:,3]
    xyz=np.stack([r*np.sqrt(1-c*c)*np.cos(a),r*np.sqrt(1-c*c)*np.sin(a),r*c],axis=1)
    dt=t[:,None]-t[None,:]
    dist=np.linalg.norm(xyz[:,None,:]-xyz[None,:,:],axis=2)
    pred=[sum(1<<i for i in range(N) if dt[j,i]>dist[j,i]) for j in range(N)]
    return pred

def analyze(pred):
    N=len(pred);full=(1<<N)-1
    h0=sum(x==0 for x in pred);h1=sum(x.bit_count()==1 for x in pred)
    if (1<<N)>args.maxstates:return None
    @lru_cache(maxsize=None)
    def ext(rem):
        if rem==0:return 1
        total=0
        for i in range(N):
            bit=1<<i
            if rem & bit and not (pred[i]&rem):total+=ext(rem^bit)
        return total
    e=ext(full)
    A=B=0;num_chain=num_anti=0
    for i in range(N):
      for j in range(i+1,N):
        rem=full^(1<<i)^(1<<j)
        if (pred[i]&rem) or (pred[j]&rem):continue
        # An ideal cannot exclude any predecessor; the remaining pred would
        # imply an excluded predecessor, so require none.
        if pred[i]&~((1<<i)|(1<<j)):continue
        if pred[j]&~((1<<i)|(1<<j)):continue
        w=ext(rem)
        if pred[i]&(1<<j) or pred[j]&(1<<i):A+=w;num_chain+=1
        else:B+=w;num_anti+=1
    assert A+2*B==e,(A,B,e)
    assert num_chain==h1 and num_anti==comb(h0,2)
    return (Q(A,e),Q(A,num_chain)/Q(B,num_anti) if A and B else None,h0,h1,ext.cache_info().currsize)

if __name__=='__main__':
    plan=[(8,120),(12,90),(16,40),(18,20),(20,12)]
    for N,reps in plan:
        start=perf_counter();rows=[]
        for k in range(reps):
            v=analyze(sample(N))
            if v is None:raise SystemExit('RESOURCE_GUARD: INCOMPLETE')
            rows.append(v)
        ps=[float(x[0]) for x in rows]
        rs=[float(x[1]) for x in rows if x[1] is not None]
        print('N',N,'REPS',reps,'P_MEAN',round(mean(ps),8),'P_MEDIAN',round(median(ps),8),
              'RATIO_MEAN',round(mean(rs),5) if rs else None,'H0_MEAN',round(mean(x[2] for x in rows),3),
              'H1_MEAN',round(mean(x[3] for x in rows),3),'MAX_DP_STATES',max(x[4] for x in rows),
              'WALL_SEC',round(perf_counter()-start,2),flush=True)
    print('FINITE_EVIDENCE_ONLY := YES')
    print('GROWTH_LIMIT := OPEN')
